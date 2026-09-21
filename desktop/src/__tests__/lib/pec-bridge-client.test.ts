import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import * as pecBridgeClientModule from '../../lib/harness/mcp/pec-bridge-client';
import {
  PEC_BRIDGE_MAX_CSV_BYTES,
  PEC_STALE_PROPOSAL_GUIDANCE,
  PecBridgeClient,
  PecBridgeError,
  resolvePecBridgeConfig
} from '../../lib/harness/mcp/pec-bridge-client';

const SENTINEL_EMAIL = 'sentinel-agent-email@rehearsal.test';
const SENTINEL_PASSWORD = 'sentinel-agent-password-3f9c';
const SENTINEL_COOKIE_TOKEN = 'sentinel-cookie-token-a1b2c3d4';

type RecordedRequest = {
  url: string;
  init: RequestInit;
};

let requests: RecordedRequest[];
let fetchMock: ReturnType<typeof vi.fn>;

function jsonResponse(status: number, body: unknown, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json', ...headers }
  });
}

function loginOkResponse(): Response {
  return jsonResponse(
    200,
    { me: { personId: 16, email: SENTINEL_EMAIL, isAdmin: false } },
    { 'set-cookie': `pec_session=${SENTINEL_COOKIE_TOKEN}; HttpOnly; SameSite=Lax; Path=/` }
  );
}

function enqueueResponses(...responses: Response[]): void {
  for (const response of responses) {
    fetchMock.mockImplementationOnce(async (url: string | URL, init?: RequestInit) => {
      requests.push({ url: String(url), init: init ?? {} });
      return response;
    });
  }
}

async function serializedError(promise: Promise<unknown>): Promise<{
  error: PecBridgeError;
  serialized: string;
}> {
  let caught: unknown;
  try {
    await promise;
  } catch (error) {
    caught = error;
  }
  expect(caught).toBeInstanceOf(PecBridgeError);
  const error = caught as PecBridgeError;
  const serialized = [
    JSON.stringify({ ...error, engineError: error.engineError }),
    error.message,
    error.stack ?? ''
  ].join('\n');
  return { error, serialized };
}

beforeEach(() => {
  requests = [];
  fetchMock = vi.fn(async (url: string | URL, init?: RequestInit) => {
    requests.push({ url: String(url), init: init ?? {} });
    throw new Error(`unexpected fetch call: ${String(url)}`);
  });
  vi.stubGlobal('fetch', fetchMock);
  vi.stubEnv('CHIRALITY_PEC_AGENT_EMAIL', SENTINEL_EMAIL);
  vi.stubEnv('CHIRALITY_PEC_AGENT_PASSWORD', SENTINEL_PASSWORD);
});

afterEach(() => {
  vi.unstubAllGlobals();
  vi.unstubAllEnvs();
});

describe('resolvePecBridgeConfig', () => {
  it('defaults to port 4810 and honors CHIRALITY_PEC_PORT', () => {
    expect(resolvePecBridgeConfig({})).toEqual({ port: 4810 });
    expect(resolvePecBridgeConfig({ CHIRALITY_PEC_PORT: '4899' })).toEqual({ port: 4899 });
  });

  it('refuses garbage and out-of-range ports', () => {
    for (const value of ['nope', '0', '65536', '-1', '80.5']) {
      expect(() => resolvePecBridgeConfig({ CHIRALITY_PEC_PORT: value })).toThrowError(
        /CHIRALITY_PEC_PORT must be an integer between 1 and 65535/
      );
    }
  });
});

describe('PecBridgeClient endpoint allowlist and loopback construction', () => {
  it('exports exactly the allowlisted surface with no generic request function', () => {
    expect(Object.keys(pecBridgeClientModule).sort()).toEqual([
      'PEC_BRIDGE_DEFAULT_PORT',
      'PEC_BRIDGE_LOOPBACK_HOST',
      'PEC_BRIDGE_MAX_CSV_BYTES',
      'PEC_STALE_PROPOSAL_GUIDANCE',
      'PecBridgeClient',
      'PecBridgeError',
      'resolvePecBridgeConfig'
    ]);
    // The instance surface is exactly the four allowlisted operations plus
    // dispose/endpointDescriptor; no request(method, path) exists anywhere.
    expect(Object.getOwnPropertyNames(PecBridgeClient.prototype).sort()).toEqual([
      'constructor',
      'createProposal',
      'dispose',
      'endpointDescriptor',
      'getProposal',
      'login',
      'refreshProposal'
    ]);
  });

  it('always targets http://127.0.0.1:<port>, ignores host-like config, and refuses redirects', async () => {
    // No constructor path accepts a host: extra properties are ignored by shape.
    const client = new PecBridgeClient({
      port: 4899,
      host: 'pec.example.com',
      baseUrl: 'http://evil.example.com'
    } as unknown as { port: number });
    expect(client.endpointDescriptor()).toEqual({ host: '127.0.0.1', port: 4899 });

    enqueueResponses(loginOkResponse(), jsonResponse(200, { id: 9 }));
    await client.getProposal(2, 9);

    expect(requests.map((request) => request.url)).toEqual([
      'http://127.0.0.1:4899/api/auth/login',
      'http://127.0.0.1:4899/api/projects/2/import-proposals/9'
    ]);
    for (const request of requests) {
      expect(request.init.redirect).toBe('error');
    }
    expect(() => new PecBridgeClient({ port: 0 })).toThrowError(
      /port must be an integer between 1 and 65535/
    );
  });

  it('builds the propose call shape: encoded query params, {csv} JSON body, no Origin header', async () => {
    const client = new PecBridgeClient({ port: 4899 });
    enqueueResponses(loginOkResponse(), jsonResponse(200, { id: 1, ref: 'IPR-0001' }));

    await client.createProposal(2, 'mdl', 'doc_no,title\nA,B\n', 'weekly drop & review.csv');

    const propose = requests[1];
    expect(propose.url).toBe(
      'http://127.0.0.1:4899/api/projects/2/import-proposals?contract=mdl&filename=weekly+drop+%26+review.csv'
    );
    expect(propose.init.method).toBe('POST');
    expect(JSON.parse(String(propose.init.body))).toEqual({ csv: 'doc_no,title\nA,B\n' });
    const headers = propose.init.headers as Record<string, string>;
    expect(Object.keys(headers).map((key) => key.toLowerCase())).not.toContain('origin');
    expect(headers['content-type']).toBe('application/json');
    expect(headers.cookie).toBe(`pec_session=${SENTINEL_COOKIE_TOKEN}`);
  });

  it('refreshProposal and getProposal use their hard-coded method+path templates', async () => {
    const client = new PecBridgeClient({ port: 4899 });
    enqueueResponses(
      loginOkResponse(),
      jsonResponse(200, { id: 9, version: 3 }),
      jsonResponse(200, { id: 9, version: 3 })
    );

    await client.refreshProposal(2, 9, 2);
    await client.getProposal(2, 9);

    expect(requests[1].url).toBe('http://127.0.0.1:4899/api/projects/2/import-proposals/9/refresh');
    expect(requests[1].init.method).toBe('POST');
    expect(JSON.parse(String(requests[1].init.body))).toEqual({ version: 2 });
    expect(requests[2].url).toBe('http://127.0.0.1:4899/api/projects/2/import-proposals/9');
    expect(requests[2].init.method).toBe('GET');
    expect(requests[2].init.body).toBeUndefined();
  });

  it('refuses non-integer record ids client-side before any network call', async () => {
    const client = new PecBridgeClient({ port: 4899 });
    await expect(client.getProposal(2.5, 9)).rejects.toMatchObject({
      errorClass: 'bad_request'
    });
    await expect(client.refreshProposal(2, 9, 1.5)).rejects.toMatchObject({
      errorClass: 'bad_request'
    });
    expect(fetchMock).not.toHaveBeenCalled();
  });
});

describe('PecBridgeClient 401 re-login cycle', () => {
  it('re-logs-in once, retries once, and succeeds', async () => {
    const client = new PecBridgeClient({ port: 4899 });
    enqueueResponses(
      loginOkResponse(),
      jsonResponse(401, { error: { code: 'UNAUTHORIZED', message: 'authentication required' } }),
      loginOkResponse(),
      jsonResponse(200, { id: 9, version: 1 })
    );

    await expect(client.getProposal(2, 9)).resolves.toEqual({ id: 9, version: 1 });
    expect(fetchMock).toHaveBeenCalledTimes(4);
    expect(requests.map((request) => request.url.endsWith('/api/auth/login'))).toEqual([
      true,
      false,
      true,
      false
    ]);
  });

  it('reports auth_failed after a second 401 with exactly one retry', async () => {
    const client = new PecBridgeClient({ port: 4899 });
    enqueueResponses(
      loginOkResponse(),
      jsonResponse(401, { error: { code: 'UNAUTHORIZED', message: 'authentication required' } }),
      loginOkResponse(),
      jsonResponse(401, { error: { code: 'UNAUTHORIZED', message: 'authentication required' } })
    );

    await expect(client.getProposal(2, 9)).rejects.toMatchObject({
      errorClass: 'auth_failed',
      status: 401
    });
    // login, data, re-login, single retry — nothing more.
    expect(fetchMock).toHaveBeenCalledTimes(4);
  });
});

describe('PecBridgeClient error taxonomy (zero retries beyond the 401 cycle)', () => {
  async function primedClient(): Promise<PecBridgeClient> {
    const client = new PecBridgeClient({ port: 4899 });
    enqueueResponses(loginOkResponse(), jsonResponse(200, { id: 1 }));
    await client.getProposal(2, 1);
    requests = [];
    fetchMock.mockClear();
    return client;
  }

  const cases: Array<{
    status: number;
    engine: { code: string; message: string; details?: unknown };
    expected: Record<string, unknown>;
  }> = [
    {
      status: 400,
      engine: { code: 'BAD_REQUEST', message: 'unknown import contract: nope' },
      expected: { errorClass: 'bad_request', status: 400, normalFlow: false }
    },
    {
      status: 403,
      engine: { code: 'FORBIDDEN', message: 'import.propose: proposing an import requires admin' },
      expected: { errorClass: 'forbidden', status: 403, normalFlow: false }
    },
    {
      status: 403,
      engine: { code: 'CROSS_ORIGIN', message: 'cross-origin request refused (RV-21)' },
      expected: { errorClass: 'forbidden', status: 403, normalFlow: false }
    },
    {
      status: 404,
      engine: { code: 'NOT_FOUND', message: 'import_proposal #99' },
      expected: { errorClass: 'not_found', status: 404, normalFlow: false }
    },
    {
      status: 409,
      engine: {
        code: 'STALE_PROPOSAL',
        message: "the project changed since this proposal's dry-run; refresh the dry-run and re-review (RV-13)",
        details: { basisHistoryId: 226, currentWatermark: 231 }
      },
      expected: {
        errorClass: 'stale_proposal',
        status: 409,
        normalFlow: true,
        guidance: PEC_STALE_PROPOSAL_GUIDANCE
      }
    },
    {
      status: 409,
      engine: { code: 'VERSION_CONFLICT', message: 'version conflict' },
      expected: { errorClass: 'version_conflict', status: 409, normalFlow: false }
    },
    {
      status: 500,
      engine: { code: 'INTERNAL', message: 'internal server error' },
      expected: { errorClass: 'server_error', status: 500, normalFlow: false }
    }
  ];

  for (const testCase of cases) {
    it(`maps ${testCase.status} ${testCase.engine.code} with a single call`, async () => {
      const client = await primedClient();
      enqueueResponses(jsonResponse(testCase.status, { error: testCase.engine }));

      const { error } = await serializedError(client.getProposal(2, 1));
      expect(error).toMatchObject(testCase.expected);
      expect(error.engineError).toEqual(testCase.engine);
      // Zero retries: exactly one request left the client for this call.
      expect(fetchMock).toHaveBeenCalledTimes(1);
    });
  }

  it('maps network/socket failure to network_error with zero retries', async () => {
    const client = await primedClient();
    fetchMock.mockImplementationOnce(async (url: string | URL) => {
      requests.push({ url: String(url), init: {} });
      throw new TypeError('fetch failed: ECONNREFUSED');
    });

    const { error } = await serializedError(client.getProposal(2, 1));
    expect(error).toMatchObject({ errorClass: 'network_error', normalFlow: false });
    expect(fetchMock).toHaveBeenCalledTimes(1);
  });

  it('preserves 409 STALE_PROPOSAL as normal flow with the exact ruled guidance', () => {
    expect(PEC_STALE_PROPOSAL_GUIDANCE).toBe(
      'refresh the dry-run; a human re-reviews and re-accepts in pec'
    );
  });
});

describe('PecBridgeClient secret handling (packet rider 2)', () => {
  it('never exposes credentials or the cookie token in any thrown error', async () => {
    const client = new PecBridgeClient({ port: 4899 });

    // (a) missing credentials
    vi.stubEnv('CHIRALITY_PEC_AGENT_EMAIL', '');
    const missing = await serializedError(client.login());
    expect(missing.error.errorClass).toBe('auth_failed');
    vi.stubEnv('CHIRALITY_PEC_AGENT_EMAIL', SENTINEL_EMAIL);

    // (b) rejected login (response body is never mapped into the error)
    enqueueResponses(
      jsonResponse(401, {
        error: { code: 'UNAUTHORIZED', message: `invalid credentials for ${SENTINEL_EMAIL}` }
      })
    );
    const rejected = await serializedError(client.login());
    expect(rejected.error.errorClass).toBe('auth_failed');

    // (c) engine payload that echoes secret material gets scrubbed
    enqueueResponses(
      loginOkResponse(),
      jsonResponse(400, {
        error: {
          code: 'BAD_REQUEST',
          message: `echo ${SENTINEL_EMAIL} ${SENTINEL_PASSWORD}`,
          details: { echoedCookie: SENTINEL_COOKIE_TOKEN }
        }
      })
    );
    const scrubbed = await serializedError(client.getProposal(2, 1));
    expect(scrubbed.error.errorClass).toBe('bad_request');
    expect(scrubbed.error.engineError?.message).toContain('[redacted]');

    // (d) network error while a cookie is held
    fetchMock.mockImplementationOnce(async () => {
      throw new TypeError(`connect failed carrying ${SENTINEL_COOKIE_TOKEN}`);
    });
    const network = await serializedError(client.getProposal(2, 1));
    expect(network.error.errorClass).toBe('network_error');

    for (const { serialized } of [missing, rejected, scrubbed, network]) {
      expect(serialized).not.toContain(SENTINEL_EMAIL);
      expect(serialized).not.toContain(SENTINEL_PASSWORD);
      expect(serialized).not.toContain(SENTINEL_COOKIE_TOKEN);
    }
  });

  it('discards the login response body and keeps the cookie unreachable from the public API', async () => {
    const client = new PecBridgeClient({ port: 4899 });
    enqueueResponses(loginOkResponse());

    await expect(client.login()).resolves.toBeUndefined();
    // Private fields do not serialize and no public property carries the token.
    expect(JSON.stringify(client)).toBe('{}');
    expect(Object.keys(client as unknown as Record<string, unknown>)).toEqual([]);
    expect(JSON.stringify(Object.entries(client))).not.toContain(SENTINEL_COOKIE_TOKEN);

    client.dispose();
    // After dispose the next call must re-login (cookie was discarded).
    enqueueResponses(loginOkResponse(), jsonResponse(200, { id: 1 }));
    await client.getProposal(2, 1);
    expect(requests[requests.length - 2].url).toContain('/api/auth/login');
  });
});

describe('PecBridgeClient CSV cap (RV-14 mirror)', () => {
  it('refuses a CSV over 5 MiB client-side without any network call', async () => {
    const client = new PecBridgeClient({ port: 4899 });
    const oversized = 'a'.repeat(PEC_BRIDGE_MAX_CSV_BYTES + 1);

    await expect(client.createProposal(2, 'mdl', oversized)).rejects.toMatchObject({
      errorClass: 'bad_request',
      normalFlow: false
    });
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
