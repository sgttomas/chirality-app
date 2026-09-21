import { createServer, type Server, type ServerResponse } from 'node:http';
import type { Socket } from 'node:net';

export type FakeModelResponse =
  | { kind: 'json'; status?: number; body: unknown }
  | { kind: 'raw'; status?: number; contentType?: string; body: string }
  | { kind: 'redirect'; location: string };

export type FakeCompletionResponse =
  | { kind: 'sse'; values: readonly unknown[]; includeDone?: boolean }
  | { kind: 'raw'; status?: number; contentType?: string; body: string }
  | { kind: 'error'; status: number; body: unknown }
  | { kind: 'disconnect'; body?: string }
  | { kind: 'hang'; started?: () => void }
  | { kind: 'redirect'; location: string };

export type FakeOpenAiLoopback = {
  baseUrl: string;
  posts: Array<Record<string, unknown>>;
  completionCount: () => number;
  close: () => Promise<void>;
};

export function completionChunk(
  model: string,
  delta: Record<string, unknown>,
  finishReason: string | null = null
): Record<string, unknown> {
  return {
    id: 'chatcmpl_chirality_fake',
    object: 'chat.completion.chunk',
    created: 1,
    model,
    choices: [{ index: 0, delta, finish_reason: finishReason }]
  };
}

function sendSse(
  response: ServerResponse,
  values: readonly unknown[],
  includeDone = true
): void {
  response.writeHead(200, { 'content-type': 'text/event-stream' });
  for (const value of values) {
    response.write(`data: ${JSON.stringify(value)}\n\n`);
  }
  if (includeDone) {
    response.end('data: [DONE]\n\n');
  } else {
    response.end();
  }
}

export async function startFakeOpenAiLoopback(input: {
  apiKey: string;
  models: FakeModelResponse;
  completions?: readonly FakeCompletionResponse[];
}): Promise<FakeOpenAiLoopback> {
  const posts: Array<Record<string, unknown>> = [];
  const sockets = new Set<Socket>();
  const hungResponses = new Set<ServerResponse>();
  let completionCount = 0;
  const server: Server = createServer(async (request, response) => {
    if (request.headers.authorization !== `Bearer ${input.apiKey}`) {
      response.writeHead(401, { 'content-type': 'application/json' });
      response.end(JSON.stringify({ error: { message: 'unauthorized' } }));
      return;
    }

    if (request.method === 'GET' && request.url === '/v1/models') {
      if (input.models.kind === 'redirect') {
        response.writeHead(302, { location: input.models.location }).end();
      } else if (input.models.kind === 'raw') {
        response.writeHead(input.models.status ?? 200, {
          'content-type': input.models.contentType ?? 'application/json'
        });
        response.end(input.models.body);
      } else {
        response.writeHead(input.models.status ?? 200, { 'content-type': 'application/json' });
        response.end(JSON.stringify(input.models.body));
      }
      return;
    }

    if (request.method !== 'POST' || request.url !== '/v1/chat/completions') {
      response.writeHead(404).end();
      return;
    }

    const body: Buffer[] = [];
    for await (const part of request) {
      body.push(Buffer.from(part));
    }
    const rawBody = Buffer.concat(body).toString('utf8');
    try {
      posts.push(JSON.parse(rawBody) as Record<string, unknown>);
    } catch {
      posts.push({ malformedRequestBody: rawBody });
    }

    const scripted = input.completions?.[completionCount];
    completionCount += 1;
    if (!scripted) {
      response.writeHead(500, { 'content-type': 'application/json' });
      response.end(JSON.stringify({ error: { message: 'unexpected completion request' } }));
      return;
    }
    switch (scripted.kind) {
      case 'sse':
        sendSse(response, scripted.values, scripted.includeDone);
        return;
      case 'raw':
        response.writeHead(scripted.status ?? 200, {
          'content-type': scripted.contentType ?? 'text/event-stream'
        });
        response.end(scripted.body);
        return;
      case 'error':
        response.writeHead(scripted.status, { 'content-type': 'application/json' });
        response.end(JSON.stringify(scripted.body));
        return;
      case 'disconnect':
        if (scripted.body) {
          response.writeHead(200, { 'content-type': 'text/event-stream' });
          response.write(scripted.body);
        }
        response.socket?.destroy();
        return;
      case 'hang':
        response.writeHead(200, { 'content-type': 'text/event-stream' });
        response.write(': stream-open\n\n');
        hungResponses.add(response);
        scripted.started?.();
        response.once('close', () => hungResponses.delete(response));
        return;
      case 'redirect':
        response.writeHead(307, { location: scripted.location }).end();
        return;
    }
  });
  server.on('connection', (socket) => {
    sockets.add(socket);
    socket.once('close', () => sockets.delete(socket));
  });
  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  const address = server.address();
  if (!address || typeof address === 'string') {
    throw new Error('Fake provider has no loopback port');
  }
  return {
    baseUrl: `http://127.0.0.1:${address.port}/v1`,
    posts,
    completionCount: () => completionCount,
    async close() {
      for (const response of hungResponses) {
        response.destroy();
      }
      for (const socket of sockets) {
        socket.destroy();
      }
      if (!server.listening) {
        return;
      }
      await new Promise<void>((resolve) => server.close(() => resolve()));
    }
  };
}
