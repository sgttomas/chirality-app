import { createServer, type Server, type ServerResponse } from 'node:http';
import type { AddressInfo } from 'node:net';
import { afterEach, describe, expect, it } from 'vitest';
import {
  DEFAULT_OMLX_BASE_URL,
  OmlxProviderError,
  discoverOmlxModels,
  normalizeOmlxBaseUrl,
  requireOmlxModel
} from '../../lib/harness/omlx-provider-config';

const SECRET = 'omlx-test-secret-never-report';
const servers: Server[] = [];

async function startServer(
  handler: (requestUrl: string, authorization: string | undefined, response: ServerResponse) => void
): Promise<string> {
  const server = createServer((request, response) => {
    handler(request.url ?? '', request.headers.authorization, response);
  });
  servers.push(server);
  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      server.off('error', reject);
      resolve();
    });
  });
  const address = server.address() as AddressInfo;
  return `http://127.0.0.1:${address.port}/v1`;
}

afterEach(async () => {
  await Promise.all(
    servers.splice(0).map(
      (server) =>
        new Promise<void>((resolve, reject) =>
          server.close((error) => (error ? reject(error) : resolve()))
        )
    )
  );
  delete process.env.CHIRALITY_OMLX_API_KEY;
});

describe('oMLX provider configuration', () => {
  it('defaults to the authenticated literal-loopback v1 endpoint', () => {
    expect(normalizeOmlxBaseUrl()).toBe(DEFAULT_OMLX_BASE_URL);
  });

  it.each([
    'https://127.0.0.1:8000/v1',
    'http://localhost:8000/v1',
    'http://2130706433:8000/v1',
    'http://user:pass@127.0.0.1:8000/v1',
    'http://127.0.0.1:8000/v1/models',
    'http://127.0.0.1:8000/v1?key=value',
    'http://127.0.0.1:8000/v1#fragment'
  ])('rejects unsafe or unexpected endpoint %s', (value) => {
    expect(() => normalizeOmlxBaseUrl(value)).toThrowError(OmlxProviderError);
  });

  it('discovers exact model IDs with the oMLX bearer key', async () => {
    let seenAuthorization: string | undefined;
    const baseUrl = await startServer((requestUrl, authorization, response) => {
      seenAuthorization = authorization;
      expect(requestUrl).toBe('/v1/models');
      response.writeHead(200, { 'content-type': 'application/json' });
      response.end(JSON.stringify({ data: [{ id: 'mlx-community/Qwen3-Coder-30B-A3B-4bit' }] }));
    });

    await expect(discoverOmlxModels({ baseUrl, apiKey: SECRET })).resolves.toEqual([
      'mlx-community/Qwen3-Coder-30B-A3B-4bit'
    ]);
    expect(seenAuthorization).toBe(`Bearer ${SECRET}`);
  });

  it('refuses redirects before following them', async () => {
    const baseUrl = await startServer((_requestUrl, _authorization, response) => {
      response.writeHead(302, { location: 'http://example.com/models' });
      response.end();
    });

    await expect(discoverOmlxModels({ baseUrl, apiKey: SECRET })).rejects.toMatchObject({
      code: 'OMLX_PROTOCOL',
      status: 302
    });
  });

  it.each([
    [401, 'OMLX_AUTHENTICATION'],
    [403, 'OMLX_AUTHENTICATION'],
    [500, 'OMLX_PROTOCOL']
  ] as const)('returns a typed and redacted error for HTTP %i', async (status, code) => {
    const baseUrl = await startServer((_requestUrl, _authorization, response) => {
      response.writeHead(status, { 'content-type': 'text/plain' });
      response.end(`failure ${SECRET}`);
    });

    const error = await discoverOmlxModels({ baseUrl, apiKey: SECRET }).catch((caught) => caught);
    expect(error).toMatchObject({ code, status });
    expect(String(error)).not.toContain(SECRET);
  });

  it('types malformed, empty, unknown-model, and offline failures without key leakage', async () => {
    const malformedBaseUrl = await startServer((_requestUrl, _authorization, response) => {
      response.writeHead(200, { 'content-type': 'application/json' });
      response.end('{not-json');
    });
    const emptyBaseUrl = await startServer((_requestUrl, _authorization, response) => {
      response.writeHead(200, { 'content-type': 'application/json' });
      response.end(JSON.stringify({ data: [] }));
    });
    const modelsBaseUrl = await startServer((_requestUrl, _authorization, response) => {
      response.writeHead(200, { 'content-type': 'application/json' });
      response.end(JSON.stringify({ data: [{ id: 'exact-model-id' }] }));
    });

    await expect(discoverOmlxModels({ baseUrl: malformedBaseUrl, apiKey: SECRET })).rejects
      .toMatchObject({ code: 'OMLX_MODELS_MALFORMED' });
    await expect(discoverOmlxModels({ baseUrl: emptyBaseUrl, apiKey: SECRET })).rejects
      .toMatchObject({ code: 'OMLX_MODELS_EMPTY' });
    await expect(requireOmlxModel('alias', { baseUrl: modelsBaseUrl, apiKey: SECRET })).rejects
      .toMatchObject({ code: 'OMLX_MODEL_UNKNOWN' });

    const offline = await discoverOmlxModels({
      apiKey: SECRET,
      fetchImpl: async () => {
        throw new Error(`network failed with ${SECRET}`);
      }
    }).catch((caught) => caught);
    expect(offline).toMatchObject({ code: 'OMLX_OFFLINE' });
    expect(String(offline)).not.toContain(SECRET);
  });
});
