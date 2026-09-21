import {
  APP_UPDATE_ALLOWED_FEED_HOSTS,
  APP_UPDATE_FEED_URL,
  APP_UPDATE_RELEASE_ROOT,
  describeAppUpdateSource,
  isAllowlistedFeedHost,
  type AppUpdateSource
} from './app-update-source';
import type {
  AppUpdateAvailable,
  AppUpdateFailure,
  AppUpdateOpenDownloadResult,
  AppUpdateState
} from './app-update-ipc-contract';

/** Minimal fetch-like response the checker needs. `Response` satisfies it. */
export type AppUpdateFetchResponse = {
  ok: boolean;
  status: number;
  text: () => Promise<string>;
  redirected?: boolean;
  url?: string;
};

export type AppUpdateFetch = (url: string, init?: RequestInit) => Promise<AppUpdateFetchResponse>;

/** Validated release information derived from the public GitHub response. */
export type AppUpdateFeed = {
  version: string;
  downloadUrl: string;
  releaseNotesUrl?: string;
  publishedAt?: string;
};

export type AppUpdateCheckResult =
  | { status: 'up-to-date'; checkedAt: string }
  | { status: 'update-available'; checkedAt: string; available: AppUpdateAvailable }
  | { status: 'failed'; checkedAt: string; failure: AppUpdateFailure };

export type AppUpdateCheckOptions = {
  source: AppUpdateSource | null;
  currentVersion: string;
  fetchImpl: AppUpdateFetch;
  allowedHosts?: readonly string[];
  platform?: string;
  arch?: string;
  timeoutMs?: number;
  now?: () => Date;
};

// ---------------------------------------------------------------------------
// Semantic versions (semver 2.0.0 precedence, build metadata ignored)
// ---------------------------------------------------------------------------

export type ParsedSemver = {
  major: number | bigint;
  minor: number | bigint;
  patch: number | bigint;
  prerelease: Array<string | number | bigint>;
};

const SEMVER_PATTERN =
  /^v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$/u;

export function parseSemver(value: string): ParsedSemver | null {
  const match = SEMVER_PATTERN.exec(value.trim());
  if (!match) return null;
  if ((match[4] ?? '').split('.').some((part) => /^0\d+$/u.test(part))) return null;
  const numeric = (part: string): number | bigint => Number.isSafeInteger(Number(part)) ? Number(part) : BigInt(part);
  const prerelease = (match[4] ?? '')
    .split('.')
    .filter((part) => part.length > 0)
    .map((part) => (/^(0|[1-9]\d*)$/u.test(part) ? numeric(part) : part));
  return {
    major: numeric(match[1]),
    minor: numeric(match[2]),
    patch: numeric(match[3]),
    prerelease
  };
}

function comparePrereleaseIdentifier(a: string | number | bigint, b: string | number | bigint): number {
  if (typeof a !== 'string' && typeof b !== 'string') return a === b ? 0 : a < b ? -1 : 1;
  // Numeric identifiers always have lower precedence than alphanumeric ones.
  if (typeof a !== 'string') return -1;
  if (typeof b !== 'string') return 1;
  return a === b ? 0 : a < b ? -1 : 1;
}

/** Negative when `a` precedes `b`, positive when it follows, zero when equal. */
export function compareSemver(a: ParsedSemver, b: ParsedSemver): number {
  if (a.major !== b.major) return a.major < b.major ? -1 : 1;
  if (a.minor !== b.minor) return a.minor < b.minor ? -1 : 1;
  if (a.patch !== b.patch) return a.patch < b.patch ? -1 : 1;
  // A version without a prerelease has higher precedence than one with.
  if (a.prerelease.length === 0 && b.prerelease.length === 0) return 0;
  if (a.prerelease.length === 0) return 1;
  if (b.prerelease.length === 0) return -1;
  const length = Math.min(a.prerelease.length, b.prerelease.length);
  for (let index = 0; index < length; index += 1) {
    const order = comparePrereleaseIdentifier(a.prerelease[index], b.prerelease[index]);
    if (order !== 0) return order;
  }
  // A larger set of prerelease fields has higher precedence when the prefix matches.
  return a.prerelease.length === b.prerelease.length
    ? 0
    : a.prerelease.length < b.prerelease.length
      ? -1
      : 1;
}

// ---------------------------------------------------------------------------
// Feed validation
// ---------------------------------------------------------------------------

/** Exact release page or asset within the owner-authorized repository and tag. */
function isReleaseUrl(value: unknown, tag: string, asset?: string): value is string {
  if (typeof value !== 'string') return false;
  const expected = asset === undefined
    ? `${APP_UPDATE_RELEASE_ROOT}/tag/${encodeURIComponent(tag)}`
    : `${APP_UPDATE_RELEASE_ROOT}/download/${encodeURIComponent(tag)}/${encodeURIComponent(asset)}`;
  try {
    const url = new URL(value);
    return value === expected && url.toString() === expected && !url.username && !url.password && !url.search && !url.hash;
  } catch {
    return false;
  }
}

export function parseAppUpdateFeed(
  body: string,
  platform: string = process.platform,
  arch: string = process.arch
): { ok: true; feed: AppUpdateFeed } | { ok: false; reason: string } {
  let parsed: unknown;
  try { parsed = JSON.parse(body); } catch {
    return { ok: false, reason: 'The release response is not valid JSON.' };
  }
  const invalid = (): { ok: false; reason: string } => ({ ok: false, reason: 'The public release response is malformed or contains an unapproved destination.' });
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) return invalid();
  const release = parsed as Record<string, unknown>;
  const tag = release.tag_name;
  if (typeof tag !== 'string' || tag !== tag.trim()) return invalid();
  const version = parseSemver(tag);
  if (!version || version.prerelease.length || release.draft !== false || release.prerelease !== false) return invalid();
  if (!isReleaseUrl(release.html_url, tag) || !Array.isArray(release.assets)) return invalid();
  if (typeof release.published_at !== 'string' || !Number.isFinite(Date.parse(release.published_at))) return invalid();
  let downloadUrl = release.html_url;
  // Only a clearly named build for this host can be selected. Other hosts use
  // the release page, where the user can inspect actual published support.
  const assetName = platform === 'darwin' && ['arm64', 'x64'].includes(arch)
    ? `Chirality-${tag.replace(/^v/u, '')}-${arch}.dmg` : undefined;
  let selected = false;
  for (const value of release.assets) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) return invalid();
    const asset = value as Record<string, unknown>;
    if (typeof asset.name !== 'string' || !asset.name || /[/\\]/u.test(asset.name) ||
        !isReleaseUrl(asset.browser_download_url, tag, asset.name)) return invalid();
    if (asset.name === assetName && asset.state === 'uploaded') {
      if (selected) return invalid();
      selected = true;
      downloadUrl = asset.browser_download_url;
    }
  }
  return { ok: true, feed: { version: tag.replace(/^v/u, ''), downloadUrl, releaseNotesUrl: release.html_url, publishedAt: release.published_at } };
}

// ---------------------------------------------------------------------------
// Policy gate on the feed source
// ---------------------------------------------------------------------------

/**
 * The single decision point for whether a source may be contacted: configured,
 * https, and its host on the allowlist. Shared by the checker and the
 * production fetch guard so the two cannot disagree.
 */
export function evaluateAppUpdateSourcePolicy(
  source: AppUpdateSource | null,
  allowedHosts: readonly string[] = APP_UPDATE_ALLOWED_FEED_HOSTS
): { allowed: true; feedUrl: string; hostname: string } | { allowed: false; failure: AppUpdateFailure } {
  if (!source) {
    return {
      allowed: false,
      failure: {
        code: 'no-release-source',
        message: 'No release source is configured for this build.'
      }
    };
  }
  let parsed: URL;
  try {
    parsed = new URL(source.feedUrl);
  } catch {
    return {
      allowed: false,
      failure: { code: 'policy', message: 'The configured release feed URL is not valid.' }
    };
  }
  if (source.feedUrl !== APP_UPDATE_FEED_URL || parsed.username || parsed.password || parsed.search || parsed.hash) {
    return {
      allowed: false,
      failure: { code: 'policy', message: 'The configured release source is not the approved public GitHub endpoint.' }
    };
  }
  if (!isAllowlistedFeedHost(parsed.hostname, allowedHosts)) {
    return {
      allowed: false,
      failure: {
        code: 'policy',
        message: `The release feed host "${parsed.hostname}" is not allowlisted for outbound network access.`
      }
    };
  }
  return { allowed: true, feedUrl: parsed.toString(), hostname: parsed.hostname };
}

/** Enforce the source again at the production network boundary. */
export function createPolicyGuardedFetch(options: {
  source: AppUpdateSource | null;
  allowedHosts?: readonly string[];
  fetchImpl?: AppUpdateFetch;
}): AppUpdateFetch {
  const delegate: AppUpdateFetch = options.fetchImpl ?? ((url, init) => globalThis.fetch(url, init));
  return async (url, init) => {
    const policy = evaluateAppUpdateSourcePolicy(options.source, options.allowedHosts);
    if (!policy.allowed) throw new Error('Release fetch refused: unapproved source.');
    if (url !== policy.feedUrl) throw new Error('Release fetch refused: URL is not the configured feed.');
    return delegate(url, {
      signal: init?.signal, redirect: 'error', cache: 'no-store', credentials: 'omit',
      headers: { Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' }
    });
  };
}

// ---------------------------------------------------------------------------
// One check
// ---------------------------------------------------------------------------

export async function checkForAppUpdate(options: AppUpdateCheckOptions): Promise<AppUpdateCheckResult> {
  const now = options.now ?? (() => new Date());
  const finish = (): string => now().toISOString();
  const fail = (failure: AppUpdateFailure): AppUpdateCheckResult => ({
    status: 'failed',
    checkedAt: finish(),
    failure
  });

  const policy = evaluateAppUpdateSourcePolicy(options.source, options.allowedHosts);
  if (!policy.allowed) return fail(policy.failure);

  const current = parseSemver(options.currentVersion);
  if (!current) {
    return fail({
      code: 'invalid-feed',
      message: `The installed version "${options.currentVersion}" is not a valid semantic version, so the feed cannot be compared.`
    });
  }

  const abort = new AbortController();
  let timer: ReturnType<typeof setTimeout> | undefined;
  let body: string;
  try {
    const request = async (): Promise<string> => {
      const response = await options.fetchImpl(policy.feedUrl, {
        signal: abort.signal, redirect: 'error', credentials: 'omit', cache: 'no-store',
        headers: { Accept: 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28' }
      });
      if (response.redirected || (response.url && response.url !== policy.feedUrl)) throw new Error('The release request was redirected and was refused.');
      if (!response.ok) {
        if (response.status === 404) throw new Error('No published stable release is available from the public repository.');
        if (response.status === 403 || response.status === 429) throw new Error('GitHub refused or rate-limited the release check. Try again later.');
        throw new Error(`The release request failed with HTTP ${response.status}.`);
      }
      return response.text();
    };
    body = await Promise.race([
      request(),
      new Promise<never>((_, reject) => {
        timer = setTimeout(() => { abort.abort(); reject(new Error('The release check timed out. Try again later.')); }, options.timeoutMs ?? 10_000);
      })
    ]);
  } catch (error) {
    return fail({ code: 'network', message: describeError(error, 'The public release could not be checked.') });
  } finally {
    if (timer !== undefined) clearTimeout(timer);
  }

  const feed = parseAppUpdateFeed(body, options.platform, options.arch);
  if (!feed.ok) return fail({ code: 'invalid-feed', message: feed.reason });

  const published = parseSemver(feed.feed.version);
  if (!published) return fail({ code: 'invalid-feed', message: 'The release feed has no valid semantic version.' });

  if (compareSemver(published, current) > 0) {
    return { status: 'update-available', checkedAt: finish(), available: { ...feed.feed } };
  }
  return { status: 'up-to-date', checkedAt: finish() };
}

// ---------------------------------------------------------------------------
// State owner
// ---------------------------------------------------------------------------

export type AppUpdateLogLevel = 'info' | 'warn' | 'error';

export type AppUpdateControllerOptions = {
  appVersion: string;
  source: AppUpdateSource | null;
  fetchImpl: AppUpdateFetch;
  openExternal: (url: string) => Promise<void>;
  allowedHosts?: readonly string[];
  platform?: string;
  arch?: string;
  timeoutMs?: number;
  now?: () => Date;
  log?: (level: AppUpdateLogLevel, event: string, detail?: unknown) => void;
};

export type AppUpdateController = {
  getState: () => AppUpdateState;
  /** Run a check, or join the one already in flight. Resolves with the settled state. */
  check: () => Promise<AppUpdateState>;
  /** Open the reported download in the system browser (https only). */
  openDownload: () => Promise<AppUpdateOpenDownloadResult>;
  /** Called on every state change. Returns the unsubscribe function. */
  subscribe: (listener: (state: AppUpdateState) => void) => () => void;
};

export const APP_UPDATE_CHECK_INTERVAL_MS = 6 * 60 * 60 * 1000;

/** Share the manual check's bounded request and state broadcast; never install. */
export function startAppUpdatePolling(controller: Pick<AppUpdateController, 'check'>): () => void {
  const check = async (): Promise<void> => {
    try {
      await controller.check();
    } catch {
      // An unexpected checker failure must not break startup or stop later checks.
    }
  };
  void check();
  const timer = setInterval(() => { void check(); }, APP_UPDATE_CHECK_INTERVAL_MS);
  timer.unref?.();
  return () => { clearInterval(timer); };
}

const CREDENTIALISH_PATTERN = /(?:Bearer|token|credential|api[_ -]?key)\s+\S+/giu;
const URL_PATTERN = /\bhttps?:\/\/\S+/giu;

/**
 * Error text for state and log: credential-shaped fragments and any URL are
 * removed, so a query string or a user-info segment never reaches a log line.
 */
function describeError(error: unknown, fallback: string): string {
  const message =
    error instanceof Error && error.message.trim() ? error.message.trim() : fallback;
  return message.replaceAll(CREDENTIALISH_PATTERN, '[redacted]').replaceAll(URL_PATTERN, '[url]').replaceAll(/\S*@\S*/gu, '[redacted]');
}

export function createAppUpdateController(options: AppUpdateControllerOptions): AppUpdateController {
  const now = options.now ?? (() => new Date());
  const log = options.log ?? (() => undefined);
  const listeners = new Set<(state: AppUpdateState) => void>();
  const appVersion = options.appVersion;

  let state: AppUpdateState = {
    currentVersion: appVersion,
    status: 'idle',
    releaseSource: describeAppUpdateSource(options.source)
  };
  let inFlight: Promise<AppUpdateState> | undefined;

  const publish = (next: AppUpdateState): void => {
    state = next;
    for (const listener of listeners) {
      try {
        listener(state);
      } catch (error) {
        log('warn', 'app_update.listener_failed', { reason: describeError(error, 'listener threw') });
      }
    }
  };

  const runCheck = async (): Promise<AppUpdateState> => {
    // Checking clears the previous outcome: a stale "update available" must
    // not stay on screen while a fresh answer is in flight.
    publish({
      currentVersion: appVersion,
      status: 'checking',
      checkedAt: state.checkedAt,
      releaseSource: state.releaseSource
    });
    log('info', 'app_update.check.started', {
      currentVersion: appVersion,
      sourceConfigured: state.releaseSource.configured
    });
    const result = await checkForAppUpdate({
      source: options.source,
      currentVersion: appVersion,
      fetchImpl: options.fetchImpl,
      allowedHosts: options.allowedHosts,
      platform: options.platform,
      arch: options.arch,
      timeoutMs: options.timeoutMs,
      now
    });
    const next: AppUpdateState = {
      currentVersion: appVersion,
      status: result.status,
      checkedAt: result.checkedAt,
      releaseSource: state.releaseSource
    };
    if (result.status === 'failed') next.failure = result.failure;
    if (result.status === 'update-available') next.available = result.available;
    publish(next);
    log(result.status === 'failed' ? 'warn' : 'info', 'app_update.check.completed', {
      status: result.status,
      failureCode: result.status === 'failed' ? result.failure.code : null,
      availableVersion: result.status === 'update-available' ? result.available.version : null
    });
    return state;
  };

  return {
    getState: () => state,
    check(): Promise<AppUpdateState> {
      if (inFlight) return inFlight;
      inFlight = runCheck().finally(() => {
        inFlight = undefined;
      });
      return inFlight;
    },
    async openDownload(): Promise<AppUpdateOpenDownloadResult> {
      const available = state.available;
      if (!available) {
        return { ok: false, error: 'No update download is available to open.' };
      }
      const tag = available.releaseNotesUrl?.slice(`${APP_UPDATE_RELEASE_ROOT}/tag/`.length);
      const asset = available.downloadUrl.split('/').at(-1);
      let approved = false;
      try {
        approved = !!tag && parseSemver(decodeURIComponent(tag)) !== null &&
          isReleaseUrl(available.releaseNotesUrl, decodeURIComponent(tag)) && (isReleaseUrl(available.downloadUrl, decodeURIComponent(tag)) ||
          (!!asset && isReleaseUrl(available.downloadUrl, decodeURIComponent(tag), decodeURIComponent(asset))));
      } catch { /* Invalid escaping is refused. */ }
      if (!approved) {
        log('warn', 'app_update.open_download.refused', { reason: 'unapproved-destination' });
        return { ok: false, error: 'The update destination is not an approved public release URL.' };
      }
      try {
        await options.openExternal(available.downloadUrl);
        log('info', 'app_update.open_download.opened', { version: available.version });
        return { ok: true };
      } catch (error) {
        const reason = describeError(error, 'The system browser could not be opened.');
        log('warn', 'app_update.open_download.failed', { reason });
        return { ok: false, error: reason };
      }
    },
    subscribe(listener) {
      listeners.add(listener);
      return () => {
        listeners.delete(listener);
      };
    }
  };
}
