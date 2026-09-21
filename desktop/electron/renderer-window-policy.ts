import { randomBytes } from 'node:crypto';

/**
 * Renderer window hardening policy (DEL-09-06-V3-01, G-CSP).
 *
 * Pure policy functions (testable without Electron) plus one installer applied
 * to every BrowserWindow the main process creates:
 *
 * - web preferences are asserted at creation: `contextIsolation: true`,
 *   `nodeIntegration: false`, `sandbox: true`; anything else fails closed;
 * - `setWindowOpenHandler` never lets the renderer create a child
 *   BrowserWindow. The renderer *does* ask for windows — every link in rendered
 *   chat markdown (`src/components/shell/chat-markdown.tsx`) and the
 *   navigator's "open legacy interface" link (`src/components/woven-dialogue/
 *   navigator.tsx`) use `target="_blank"` — so an `http:`/`https:` target is
 *   handed to the operating system's default browser (`shell.openExternal`,
 *   injected by `main.ts`) instead of a child window that would inherit this
 *   app's preload and IPC bridge; every other scheme is dropped. Before this
 *   policy such a click created a child BrowserWindow at the link's URL; now it
 *   opens the system browser (coordinator decision 2026-09-03, recorded in the
 *   run record). This is not app egress: nothing leaves this process.
 * - `will-navigate` and `will-redirect` allow only the app's own renderer
 *   origin over http(s) and deny everything else — `javascript:`, `file:`,
 *   `data:`, `about:`, `blob:`, foreign hosts, a different port or scheme;
 * - the packaged server creates a fresh nonce and one policy per request,
 *   presents that policy to Next before rendering, and returns the exact same
 *   policy on the response; the response hook never fabricates a packaged
 *   fallback whose nonce could disagree with the rendered document;
 * - development keeps its static policy fallback through
 *   `webRequest.onHeadersReceived`, including the allowances Next dev needs.
 *
 * The CSP is defence in depth beside the REQ-NET-001 egress allowlist in
 * `main.ts`, not a replacement for it: the egress layer is what the packaged
 * proof observes on the wire, through the main-process probe below.
 */

export type RendererWindowLog = (
  level: 'info' | 'warn' | 'error',
  event: string,
  detail?: unknown
) => void;

export const REQUIRED_RENDERER_WEB_PREFERENCES = Object.freeze({
  contextIsolation: true,
  nodeIntegration: false,
  sandbox: true
} as const);

const FORBIDDEN_RENDERER_WEB_PREFERENCES = [
  'nodeIntegrationInWorker',
  'nodeIntegrationInSubFrames',
  'webviewTag',
  'allowRunningInsecureContent',
  'enableRemoteModule',
  'experimentalFeatures'
] as const;

export type RendererWebPreferencesInput = Record<string, unknown>;

/** Throws when the preferences would weaken the renderer boundary. */
export function assertRendererWebPreferences(preferences: RendererWebPreferencesInput): void {
  const problems: string[] = [];
  if (preferences.contextIsolation !== true) problems.push('contextIsolation must be true');
  if (preferences.nodeIntegration !== false) problems.push('nodeIntegration must be false');
  if (preferences.sandbox !== true) problems.push('sandbox must be true');
  if (preferences.webSecurity === false) problems.push('webSecurity must not be disabled');
  for (const name of FORBIDDEN_RENDERER_WEB_PREFERENCES) {
    if (preferences[name] === true) problems.push(`${name} must not be enabled`);
  }
  if (problems.length > 0) {
    throw new Error(
      `Renderer window web preferences violate the hardening policy: ${problems.join('; ')}`
    );
  }
}

export type RendererWebPreferences = {
  preload: string;
  contextIsolation: true;
  nodeIntegration: false;
  sandbox: true;
};

/** The only web preferences a renderer window may be created with. */
export function rendererWebPreferences(input: { preload: string }): RendererWebPreferences {
  const preferences: RendererWebPreferences = {
    preload: input.preload,
    ...REQUIRED_RENDERER_WEB_PREFERENCES
  };
  assertRendererWebPreferences(preferences);
  return preferences;
}

export type RendererNavigationDecision =
  | { allowed: true }
  | { allowed: false; reason: 'INVALID_URL' | 'SCHEME_NOT_HTTP' | 'ORIGIN_NOT_RENDERER' };

/**
 * Renderer-initiated navigations may target only the renderer origin itself,
 * over http(s). The scheme check comes first because a `blob:` URL reports its
 * creator's origin — equal to the renderer's — while `javascript:`, `file:`,
 * `data:` and `about:` report the opaque origin `null`; none of them is a page
 * of the app. Everything at a foreign origin, port, or scheme is denied.
 */
export function evaluateRendererNavigation(
  rawUrl: string,
  rendererOrigin: string
): RendererNavigationDecision {
  let parsed: URL;
  try {
    parsed = new URL(rawUrl);
  } catch {
    return { allowed: false, reason: 'INVALID_URL' };
  }
  if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
    return { allowed: false, reason: 'SCHEME_NOT_HTTP' };
  }
  if (!rendererOrigin || parsed.origin === 'null' || parsed.origin !== rendererOrigin) {
    return { allowed: false, reason: 'ORIGIN_NOT_RENDERER' };
  }
  return { allowed: true };
}

export type WindowOpenDecision =
  | { action: 'deny'; external: true }
  | { action: 'deny'; external: false; reason: 'INVALID_URL' | 'SCHEME_NOT_HTTP' };

/**
 * A child BrowserWindow is never created (`action: 'deny'` for every request).
 * An `http:`/`https:` target is instead opened in the system browser by the
 * installer; a malformed URL or any other scheme (`javascript:`, `file:`,
 * `data:`, `blob:`, `about:`, custom) is dropped.
 */
export function evaluateWindowOpen(details: { url: string }): WindowOpenDecision {
  let parsed: URL;
  try {
    parsed = new URL(details.url);
  } catch {
    return { action: 'deny', external: false, reason: 'INVALID_URL' };
  }
  if (parsed.protocol !== 'http:' && parsed.protocol !== 'https:') {
    return { action: 'deny', external: false, reason: 'SCHEME_NOT_HTTP' };
  }
  return { action: 'deny', external: true };
}

export type RendererCspMode = 'packaged' | 'development';

const RENDERER_CSP_NONCE_BYTES = 16;
const RENDERER_CSP_NONCE_PATTERN = /^[A-Za-z0-9+/_-]+={0,2}$/;

/** A 128-bit, request-local nonce in the alphabet accepted by pinned Next. */
export function createRendererCspNonce(): string {
  return randomBytes(RENDERER_CSP_NONCE_BYTES).toString('base64');
}

function assertRendererCspNonce(nonce: string | undefined): asserts nonce is string {
  if (!nonce || !RENDERER_CSP_NONCE_PATTERN.test(nonce)) {
    throw new Error('Packaged renderer CSP requires a valid request nonce');
  }
}

/**
 * Renderer Content-Security-Policy.
 *
 * What the renderer actually needs, verified against the `npm run build` output
 * and the dev server (recorded in the DEL-09-06 evidence):
 * - packaged `script-src` uses the request nonce and never `'unsafe-inline'` or
 *   `'unsafe-eval'`. The custom server gives the same policy to Next before it
 *   renders, so Next's inline flight scripts carry the nonce. The root layout
 *   reads the same request policy for the app-owned theme bootstrap. External
 *   scripts remain restricted to `'self'`.
 * - development retains `'unsafe-inline'` and `'unsafe-eval'`: Next's dev
 *   runtime and React Refresh require them. No development posture changes.
 * - `'unsafe-eval'` only in development: Next's dev runtime and React Refresh
 *   evaluate source; the packaged renderer never gets it.
 * - `style-src 'unsafe-inline'`: two components set React `style` props (inline
 *   style attributes) and Next injects style elements in development.
 * - `connect-src 'self'` in packaged mode: the renderer talks only to its own
 *   Next server; the Anthropic and oMLX calls are made server-side by the Next
 *   server process and the daemon, never by the page. This is stricter than the
 *   REQ-NET-001 egress allowlist, which stays as the wire-level backstop. The
 *   dev server's HMR WebSocket needs the `ws:`/`wss:` form of its own origin.
 * - everything else is closed: no frames, no plugins, no foreign forms or bases,
 *   no embedding.
 */
export function buildRendererContentSecurityPolicy(options: {
  mode: RendererCspMode;
  rendererOrigin?: string;
  nonce?: string;
}): string {
  const development = options.mode === 'development';
  if (!development) {
    assertRendererCspNonce(options.nonce);
  }
  const connectSources = ["'self'"];
  if (development && options.rendererOrigin) {
    try {
      const origin = new URL(options.rendererOrigin);
      connectSources.push(`ws://${origin.host}`, `wss://${origin.host}`);
    } catch {
      // An unparseable origin adds nothing; 'self' still covers same-origin.
    }
  }
  const directives = [
    "default-src 'self'",
    development
      ? "script-src 'self' 'unsafe-inline' 'unsafe-eval'"
      : `script-src 'self' 'nonce-${options.nonce}'`,
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data:",
    "font-src 'self' data:",
    `connect-src ${connectSources.join(' ')}`,
    "worker-src 'self'",
    "manifest-src 'self'",
    "media-src 'self'",
    options.rendererOrigin ? `frame-src ${options.rendererOrigin}${ELIGIBLE_PDF_PATH}` : "frame-src 'none'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'"
  ];
  return directives.join('; ');
}

export const CONTENT_SECURITY_POLICY_HEADER = 'Content-Security-Policy';
export const RESPONSE_CLASS_HEADER = 'X-Chirality-Response-Class';
export const ELIGIBLE_PDF_RESPONSE_CLASS = 'eligible-pdf-v1';
export const ELIGIBLE_PDF_PATH = '/api/working-root/file';
export const PDF_CONTENT_SECURITY_POLICY = [
  "default-src 'none'", "script-src 'none'", "frame-src 'none'", "object-src 'none'",
  "base-uri 'none'", "form-action 'none'", "frame-ancestors 'self'"
].join('; ');

type RendererRequestHeaders = Record<string, string | string[] | undefined>;
type HeaderValue = string | string[] | number | undefined;
type HeaderBag = Record<string, HeaderValue>;
type RendererResponseHeaderSink = { setHeader(name: string, value: string | string[]): unknown };

export type ResponseHeaders = Record<string, string[]>;

function valuesForHeader(headers: HeaderBag | ResponseHeaders | undefined, wanted: string): string[] {
  const values: string[] = [];
  for (const [name, value] of Object.entries(headers ?? {})) {
    if (name.toLowerCase() !== wanted.toLowerCase() || value === undefined) continue;
    for (const item of Array.isArray(value) ? value : [value]) values.push(String(item));
  }
  return values;
}

function rawPathname(rawUrl: string): string | null {
  const match = rawUrl.match(/^https?:\/\/[^/?#]+([^?#]*)/i);
  return match ? match[1] || '/' : null;
}

function isAllowedPdfSubframe(rawUrl: string, rendererOrigin: string): boolean {
  try {
    const parsed = new URL(rawUrl);
    return parsed.origin === rendererOrigin && rawPathname(rawUrl) === ELIGIBLE_PDF_PATH &&
      parsed.pathname === ELIGIBLE_PDF_PATH && hasExactPdfSelectors(parsed);
  } catch { return false; }
}

function hasExactPdfSelectors(url: URL): boolean {
  const allowed = new Set(['projectRoot', 'path', 'target', 'content']);
  const keys = [...url.searchParams.keys()];
  return keys.every(key => allowed.has(key)) &&
    url.searchParams.getAll('projectRoot').length === 1 && url.searchParams.get('projectRoot') !== '' &&
    url.searchParams.getAll('content').length === 1 && url.searchParams.get('content') === 'pdf' &&
    url.searchParams.getAll('path').length <= 1 && url.searchParams.getAll('target').length <= 1 &&
    (url.searchParams.has('path') !== url.searchParams.has('target')) &&
    (url.searchParams.get('path') ?? url.searchParams.get('target') ?? '') !== '';
}

export type PdfResponseClassificationInput = {
  url: string; rendererOrigin: string; method: string; statusCode: number;
  responseHeaders?: HeaderBag | ResponseHeaders;
  mode: RendererCspMode; packagedBaselineCsp?: string;
};

/** The sole trusted classifier used at both renderer response boundaries. */
export function isEligiblePdfResponse(input: PdfResponseClassificationInput): boolean {
  let parsed: URL;
  try { parsed = new URL(input.url); } catch { return false; }
  if (parsed.origin !== input.rendererOrigin || rawPathname(input.url) !== ELIGIBLE_PDF_PATH ||
      parsed.pathname !== ELIGIBLE_PDF_PATH || !hasExactPdfSelectors(parsed) ||
      input.method !== 'GET' || input.statusCode !== 200) return false;
  const one = (name: string, expected: string) => {
    const values = valuesForHeader(input.responseHeaders, name);
    return values.length === 1 && values[0] === expected;
  };
  const lengths = valuesForHeader(input.responseHeaders, 'content-length');
  const policies = valuesForHeader(input.responseHeaders, CONTENT_SECURITY_POLICY_HEADER);
  const expectedPolicy = input.mode === 'packaged' ? input.packagedBaselineCsp : PDF_CONTENT_SECURITY_POLICY;
  return one(RESPONSE_CLASS_HEADER, ELIGIBLE_PDF_RESPONSE_CLASS) &&
    one('content-type', 'application/pdf') && one('content-disposition', 'inline') &&
    one('x-content-type-options', 'nosniff') && one('cache-control', 'no-store') &&
    lengths.length === 1 && /^[1-9][0-9]*$/.test(lengths[0]) &&
    valuesForHeader(input.responseHeaders, 'location').length === 0 &&
    valuesForHeader(input.responseHeaders, 'content-range').length === 0 &&
    policies.length === 1 && policies[0] === expectedPolicy;
}

function without(headers: ResponseHeaders, wanted: string): ResponseHeaders {
  return Object.fromEntries(Object.entries(headers).filter(([name]) => name.toLowerCase() !== wanted.toLowerCase()));
}

export function finalizeRendererResponseHeaders(input: PdfResponseClassificationInput, fallbackPolicy: string): ResponseHeaders {
  const eligible = isEligiblePdfResponse(input);
  let headers: ResponseHeaders = Object.fromEntries(Object.entries(input.responseHeaders ?? {}).map(([name, value]) => [
    name, (Array.isArray(value) ? value : value === undefined ? [] : [value]).map(String)
  ]));
  headers = without(without(headers, RESPONSE_CLASS_HEADER), CONTENT_SECURITY_POLICY_HEADER);
  return { ...headers, [CONTENT_SECURITY_POLICY_HEADER]: [eligible ? PDF_CONTENT_SECURITY_POLICY : fallbackPolicy] };
}

/** The only production emitter of the reserved eligible-PDF tuple. */
export function createEligiblePdfResponseHeaders(contentLength: number): Record<string, string> {
  if (!Number.isSafeInteger(contentLength) || contentLength <= 0) throw new Error('Eligible PDF requires a positive Content-Length');
  return {
    [RESPONSE_CLASS_HEADER]: ELIGIBLE_PDF_RESPONSE_CLASS,
    [CONTENT_SECURITY_POLICY_HEADER]: PDF_CONTENT_SECURITY_POLICY,
    'Content-Type': 'application/pdf', 'Content-Disposition': 'inline',
    'Content-Length': String(contentLength), 'X-Content-Type-Options': 'nosniff',
    'Cache-Control': 'no-store'
  };
}

function explicitWriteHeadEntries(headers: HeaderBag | unknown[] | undefined): Array<[string, HeaderValue]> {
  if (!headers) return [];
  if (!Array.isArray(headers)) return Object.entries(headers);
  return Array.from({ length: Math.floor(headers.length / 2) }, (_, index) => [
    String(headers[index * 2]), headers[index * 2 + 1] as HeaderValue
  ]);
}

/**
 * Build the headers that writeHead will deliver without first passing them
 * through Node's case-insensitive, replacement-based header store. Explicit
 * writeHead names replace pending names case-insensitively, as Node specifies,
 * while duplicate spellings and array items stay visible to the classifier.
 */
function effectiveWriteHeadHeaders(
  pending: HeaderBag,
  explicit: HeaderBag | unknown[] | undefined
): ResponseHeaders {
  const explicitEntries = explicitWriteHeadEntries(explicit);
  const explicitNames = new Set(explicitEntries.map(([name]) => name.toLowerCase()));
  const merged = new Map<string, { name: string; values: string[] }>();
  const append = (name: string, value: HeaderValue) => {
    if (value === undefined) return;
    const key = name.toLowerCase();
    const entry = merged.get(key) ?? { name, values: [] };
    for (const item of Array.isArray(value) ? value : [value]) entry.values.push(String(item));
    merged.set(key, entry);
  };
  for (const [name, value] of Object.entries(pending)) {
    if (!explicitNames.has(name.toLowerCase())) append(name, value);
  }
  for (const [name, value] of explicitEntries) append(name, value);
  return Object.fromEntries([...merged.values()].map(({ name, values }) => [name, values]));
}

/**
 * Establish the packaged renderer's one-policy invariant before Next handles a
 * request. The policy is derived once and assigned byte-for-byte to both the
 * incoming request and outgoing response. Next 15.5 reads the request CSP and
 * applies its nonce to framework scripts; the app layout reads that same CSP
 * for its own inline bootstrap. There is no second nonce-bearing header that
 * could disagree with the enforced policy.
 */
export function applyPackagedRendererRequestPolicy(
  request: { headers: RendererRequestHeaders; url?: string; method?: string },
  response: RendererResponseHeaderSink & {
    statusCode?: number; headersSent?: boolean; getHeaders?: () => HeaderBag;
    removeHeader?: (name: string) => void; writeHead?: (...args: any[]) => unknown;
  },
  nonce: string = createRendererCspNonce()
): { nonce: string; contentSecurityPolicy: string } {
  assertRendererCspNonce(nonce);
  const host = String(request.headers.host ?? '');
  const rendererOrigin = host ? `http://${host}` : undefined;
  const contentSecurityPolicy = buildRendererContentSecurityPolicy({ mode: 'packaged', nonce, rendererOrigin });
  request.headers[CONTENT_SECURITY_POLICY_HEADER.toLowerCase()] = contentSecurityPolicy;
  response.setHeader(CONTENT_SECURITY_POLICY_HEADER, contentSecurityPolicy);
  if (response.writeHead && response.getHeaders && response.removeHeader) {
    const getHeaders = response.getHeaders.bind(response);
    const removeHeader = response.removeHeader.bind(response);
    const originalWriteHead = response.writeHead.bind(response);
    response.writeHead = (...args: any[]) => {
      response.writeHead = originalWriteHead;
      const explicit = (args[1] !== null && typeof args[1] === 'object' ? args[1] : args[2]) as HeaderBag | unknown[] | undefined;
      const effectiveHeaders = effectiveWriteHeadHeaders(getHeaders(), explicit);
      const final = finalizeRendererResponseHeaders({
        url: `${rendererOrigin ?? 'http://invalid'}${request.url ?? '/'}`, rendererOrigin: rendererOrigin ?? '',
        method: request.method ?? 'GET', statusCode: Number(args[0] ?? response.statusCode ?? 200),
        responseHeaders: effectiveHeaders, mode: 'packaged', packagedBaselineCsp: contentSecurityPolicy
      }, contentSecurityPolicy);
      for (const name of Object.keys(getHeaders())) removeHeader(name);
      for (const [name, values] of Object.entries(final)) response.setHeader(name, values.length === 1 ? values[0] : values);
      return typeof args[1] === 'string' ? originalWriteHead(args[0], args[1]) : originalWriteHead(args[0]);
    };
  }
  return { nonce, contentSecurityPolicy };
}

function hasContentSecurityPolicy(headers: ResponseHeaders): boolean {
  return Object.keys(headers).some(
    (name) => name.toLowerCase() === CONTENT_SECURITY_POLICY_HEADER.toLowerCase()
  );
}

/**
 * Headers to install on a response from the renderer origin that carries no
 * policy, or `null` when the response must be left exactly as received (foreign
 * origin, unparseable URL, or a policy already present). Pure.
 */
export function applyContentSecurityPolicyHeader(
  details: { url: string; responseHeaders?: ResponseHeaders },
  rendererOrigin: string,
  contentSecurityPolicy: string
): ResponseHeaders | null {
  let origin: string;
  try {
    origin = new URL(details.url).origin;
  } catch {
    return null;
  }
  const headers = details.responseHeaders ?? {};
  if (origin !== rendererOrigin || hasContentSecurityPolicy(headers)) {
    return null;
  }
  return { ...headers, [CONTENT_SECURITY_POLICY_HEADER]: [contentSecurityPolicy] };
}

/** Non-secret destination summary for diagnostics: no path, query, or userinfo. */
export function summarizeDestination(rawUrl: string): { protocol: string; hostname: string } | null {
  try {
    const parsed = new URL(rawUrl);
    return { protocol: parsed.protocol, hostname: parsed.hostname };
  } catch {
    return null;
  }
}

export type RendererWindowLike = {
  webContents: {
    setWindowOpenHandler(handler: (details: { url: string }) => { action: 'deny' }): void;
    on(event: string, listener: (...args: any[]) => void): unknown;
    session: {
      webRequest: {
        onHeadersReceived(
          filter: { urls: string[] },
          listener: (
            details: { url: string; method?: string; statusCode?: number; responseHeaders?: ResponseHeaders },
            callback: (response: { responseHeaders?: ResponseHeaders }) => void
          ) => void
        ): void;
      };
    };
  };
};

export type RendererWindowPolicyOptions = {
  rendererOrigin: string;
  /** Development-only fallback. Packaged responses must carry their request nonce. */
  contentSecurityPolicy?: string;
  /** Opens an `http(s)` URL in the operating system's default browser. */
  openExternal: (url: string) => Promise<void>;
  log?: RendererWindowLog;
};

const HEADER_FILTER_URLS = ['http://*/*', 'https://*/*'];

/** Install window-open handling, navigation containment, and the CSP on one window. */
export function installRendererWindowPolicy(
  window: RendererWindowLike,
  options: RendererWindowPolicyOptions
): void {
  const { rendererOrigin, contentSecurityPolicy, openExternal, log } = options;
  const { webContents } = window;

  webContents.setWindowOpenHandler((details) => {
    const decision = evaluateWindowOpen(details);
    const destination = summarizeDestination(details.url);
    if (decision.external) {
      log?.('info', 'renderer.window_open.external_opened', { destination });
      // Deferred so a synchronous throw from the injected opener is caught the
      // same way as a rejection and can never escape the handler.
      Promise.resolve()
        .then(() => openExternal(details.url))
        .catch((error: unknown) => {
          log?.('warn', 'renderer.window_open.external_failed', {
            destination,
            error: error instanceof Error ? error.message : String(error)
          });
        });
    } else {
      log?.('warn', 'renderer.window_open.denied', { reason: decision.reason, destination });
    }
    return { action: 'deny' };
  });

  for (const eventName of ['will-navigate', 'will-redirect'] as const) {
    webContents.on(eventName, (event: { preventDefault(): void; url?: string; isMainFrame?: boolean }, legacyUrl?: string, _inPlace?: boolean, legacyMainFrame?: boolean) => {
      const url = event.url ?? legacyUrl ?? '';
      const isMainFrame = event.isMainFrame ?? legacyMainFrame ?? true;
      if (!isMainFrame && eventName !== 'will-redirect' && isAllowedPdfSubframe(url, rendererOrigin)) return;
      const decision = evaluateRendererNavigation(url, rendererOrigin);
      if (decision.allowed && isMainFrame) return;
      event.preventDefault();
      log?.('warn', 'renderer.navigation.denied', {
        event: eventName,
        reason: decision.allowed ? 'SUBFRAME_NOT_ELIGIBLE_PDF' : decision.reason,
        destination: summarizeDestination(url)
      });
    });
  }

  webContents.on('will-frame-navigate', (details: { preventDefault(): void; url: string; isMainFrame: boolean }) => {
    if (details.isMainFrame || isAllowedPdfSubframe(details.url, rendererOrigin)) return;
    details.preventDefault();
    log?.('warn', 'renderer.subframe_navigation.denied', { destination: summarizeDestination(details.url) });
  });

  webContents.session.webRequest.onHeadersReceived(
    { urls: HEADER_FILTER_URLS },
    (details, callback) => {
      let responseHeaders: ResponseHeaders | null = null;
      try {
        if (new URL(details.url).origin === rendererOrigin && contentSecurityPolicy) {
          responseHeaders = finalizeRendererResponseHeaders({
            url: details.url, rendererOrigin, method: details.method ?? 'GET',
            statusCode: details.statusCode ?? 0, responseHeaders: details.responseHeaders,
            mode: 'development'
          }, contentSecurityPolicy);
        }
      } catch { /* foreign or malformed responses remain untouched */ }
      // No override at all when untouched: echoing an empty header set would
      // tell Chromium the server answered with no headers.
      callback(responseHeaders === null ? {} : { responseHeaders });
    }
  );
}

type ProbeEnvironment = Record<string, string | undefined>;

function probeDelayMs(env: ProbeEnvironment, fallback: number): number {
  const parsed = Number.parseInt(env.CHIRALITY_RENDERER_SECURITY_PROBE_DELAY_MS ?? '', 10);
  return Number.isSafeInteger(parsed) && parsed > 0 ? parsed : fallback;
}

function afterLoad(
  webContents: { isLoadingMainFrame(): boolean; once(event: 'did-finish-load', listener: () => void): unknown },
  delayMs: number,
  run: () => void
): void {
  const schedule = (): void => {
    setTimeout(run, delayMs);
  };
  if (webContents.isLoadingMainFrame()) {
    webContents.once('did-finish-load', schedule);
  } else {
    schedule();
  }
}

/**
 * Optional in-page probe for the packaged security proof
 * (`CHIRALITY_RENDERER_SECURITY_PROBE=1`): reports the document's CSP header
 * (same-origin fetch of the page), a denied `window.open` — deliberately of an
 * `about:blank` target so the proof never opens the host's browser; the
 * `http(s)` hand-off is unit-tested — the `securitypolicyviolation` events
 * raised by a deliberately blocked fetch, and finally attempts a foreign
 * navigation so the main process logs its denial. Nothing runs unless the
 * environment asks for it. Results are written to the console under the
 * `[renderer-security-probe]` marker the proof reads.
 */
export function runRendererSecurityProbe(
  window: {
    webContents: {
      isLoadingMainFrame(): boolean;
      once(event: 'did-finish-load', listener: () => void): unknown;
      executeJavaScript(code: string, userGesture?: boolean): Promise<unknown>;
    };
  },
  options: { env: ProbeEnvironment }
): void {
  if (options.env.CHIRALITY_RENDERER_SECURITY_PROBE !== '1') {
    return;
  }
  const script = `
(() => {
  const violations = [];
  const noncePattern = /^[A-Za-z0-9+/_-]+={0,2}$/;
  const nonceFromPolicy = (policy) => {
    if (typeof policy !== 'string') return null;
    const scriptDirective = policy
      .split(';')
      .map((directive) => directive.trim())
      .find((directive) => directive.startsWith('script-src '));
    if (!scriptDirective) return null;
    for (const source of scriptDirective.split(/\\s+/).slice(1)) {
      const match = source.match(/^'nonce-([A-Za-z0-9+/_-]+={0,2})'$/);
      if (match) return match[1];
    }
    return null;
  };
  const inlineScriptNonces = (root) => Array.from(root.querySelectorAll('script'))
    .filter((node) => !node.src && (node.textContent || '').trim().length > 0)
    .map((node) => node.nonce || null);
  const inspectResponse = async () => {
    const response = await fetch(location.href, { cache: 'no-store' });
    const cspHeader = response.headers.get('content-security-policy');
    const html = await response.text();
    const responseNonce = nonceFromPolicy(cspHeader);
    const parsed = new DOMParser().parseFromString(html, 'text/html');
    const scriptNonces = inlineScriptNonces(parsed);
    return {
      status: response.status,
      contentType: response.headers.get('content-type'),
      cspHeader,
      responseNonce,
      inlineScriptCount: scriptNonces.length,
      inlineScriptNoncesMatch: scriptNonces.length > 0 &&
        scriptNonces.every((value) => value === responseNonce),
      documentComplete: html.includes('</html>')
    };
  };
  document.addEventListener('securitypolicyviolation', (event) => {
    violations.push({
      blockedURI: event.blockedURI,
      effectiveDirective: event.effectiveDirective,
      disposition: event.disposition
    });
  });
  const run = async () => {
    const documentScriptNonces = inlineScriptNonces(document);
    const documentNonce = documentScriptNonces.find((value) => noncePattern.test(value || '')) || null;
    let consecutiveResponses = [];
    let responseError = null;
    try {
      consecutiveResponses = [await inspectResponse(), await inspectResponse()];
    } catch (error) {
      responseError = error instanceof Error ? error.message : String(error);
    }
    let windowOpen;
    try {
      const opened = window.open('about:blank#chirality-renderer-security-window-open', '_blank');
      windowOpen = { returned: opened === null ? 'null' : typeof opened };
    } catch (error) {
      windowOpen = { error: error instanceof Error ? error.message : String(error) };
    }
    try {
      await fetch('https://example.com/chirality-renderer-security-csp-blocked', {
        mode: 'no-cors',
        cache: 'no-store'
      });
    } catch {
      // A rejected fetch is the expected outcome; the violation event is the evidence.
    }
    await new Promise((resolve) => setTimeout(resolve, 250));
    const navigationTarget = 'https://example.com/chirality-renderer-security-navigation';
    setTimeout(() => {
      try {
        location.assign(navigationTarget);
      } catch {
        // Denied navigation surfaces in the main-process log.
      }
    }, 0);
    return {
      policy: 'G-CSP',
      route: location.pathname,
      documentNonce: noncePattern.test(documentNonce || '') ? documentNonce : null,
      documentInlineScriptCount: documentScriptNonces.length,
      documentInlineScriptNoncesMatch: documentScriptNonces.length > 0 &&
        documentScriptNonces.every((value) => value === documentNonce),
      consecutiveResponses,
      responseError,
      windowOpen,
      violations,
      navigationAttempted: navigationTarget
    };
  };
  return run();
})();
`;
  afterLoad(window.webContents, probeDelayMs(options.env, 1500), () => {
    void window.webContents
      .executeJavaScript(script, true)
      .then((result) => {
        console.info('[renderer-security-probe]', JSON.stringify(result));
      })
      .catch((error: unknown) => {
        console.error(
          '[renderer-security-probe]',
          JSON.stringify({ policy: 'G-CSP', error: error instanceof Error ? error.message : String(error) })
        );
      });
  });
}

/**
 * The one destination the main-process egress-layer probe may request. It is
 * fixed here and never read from the environment or taken from a caller, so
 * nothing outside this module can point the probe at a destination the
 * REQ-NET-001 egress policy in `main.ts` would allow (DEL-09-06-V3-05). The
 * Anthropic API host is allowlisted only over `https:` on port 443, so the same
 * host on port 8443 is denied by the policy's port rule
 * (`anthropic_port_not_allowlisted:8443`) — exactly the denial the packaged
 * proof counts. The proof script carries the same literal as its expectation
 * and its unit test checks the two stay byte-equal.
 */
export const EGRESS_LAYER_PROBE_URL =
  'https://api.anthropic.com:8443/chirality-packaged-security-egress-blocked';

/**
 * Optional main-process probe of the REQ-NET-001 egress layer for the packaged
 * security proof (same gate as the in-page probe; the destination is
 * `EGRESS_LAYER_PROBE_URL`, always). The page cannot reach the egress layer for
 * a foreign host any more — the CSP stops it first — so the proof issues the
 * request from the main process through the window's session: `session.fetch`
 * goes through `webRequest`, where `onBeforeRequest` cancels it and logs the
 * denial. A rejected fetch is the expected outcome; a response would mean the
 * egress layer let it through. The logged destination carries protocol,
 * hostname, and port (the port is what makes it a denied destination) and no
 * path.
 */
export function runEgressLayerProbe(
  window: {
    webContents: {
      isLoadingMainFrame(): boolean;
      once(event: 'did-finish-load', listener: () => void): unknown;
      session: {
        fetch(
          input: string,
          init?: { method?: string; cache?: 'no-store'; signal?: AbortSignal }
        ): Promise<{ status: number }>;
      };
    };
  },
  options: { env: ProbeEnvironment }
): void {
  if (options.env.CHIRALITY_RENDERER_SECURITY_PROBE !== '1') {
    return;
  }
  const parsed = new URL(EGRESS_LAYER_PROBE_URL);
  const destination = { protocol: parsed.protocol, hostname: parsed.hostname, port: parsed.port };
  afterLoad(window.webContents, probeDelayMs(options.env, 1500) + 500, () => {
    void window.webContents.session
      .fetch(EGRESS_LAYER_PROBE_URL, {
        method: 'GET',
        cache: 'no-store',
        signal: AbortSignal.timeout(3000)
      })
      .then((response) => {
        console.info(
          '[egress-layer-probe]',
          JSON.stringify({ policy: 'REQ-NET-001', destination, outcome: 'response', status: response.status })
        );
      })
      .catch((error: unknown) => {
        console.info(
          '[egress-layer-probe]',
          JSON.stringify({
            policy: 'REQ-NET-001',
            destination,
            outcome: 'rejected',
            error: error instanceof Error ? error.message : String(error)
          })
        );
      });
  });
}
