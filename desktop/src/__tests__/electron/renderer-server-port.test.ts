import { createServer, type Server } from 'node:http';
import { chmod, mkdtemp, readFile, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { afterEach, describe, expect, it } from 'vitest';
import {
  bindStableRendererServer,
  RENDERER_PORT_RECORD_FILENAME,
  RENDERER_PORT_RECORD_SCHEMA,
  type BoundRendererServer
} from '../../../electron/renderer-server-port';

const temporaryDirectories: string[] = [];

async function temporaryUserData(): Promise<string> {
  const directory = await mkdtemp(path.join(tmpdir(), 'chirality-renderer-port-'));
  temporaryDirectories.push(directory);
  return directory;
}

async function bindHttpServer(port: number): Promise<BoundRendererServer> {
  const server = createServer((_request, response) => response.end('ok'));
  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen(port, '127.0.0.1', () => {
      server.off('error', reject);
      resolve();
    });
  });
  const address = server.address();
  if (!address || typeof address === 'string') throw new Error('test server did not bind');
  return {
    port: address.port,
    close: () => new Promise<void>((resolve, reject) => {
      server.close(error => error ? reject(error) : resolve());
    })
  };
}

async function occupy(port: number): Promise<Server> {
  const server = createServer();
  await new Promise<void>((resolve, reject) => {
    server.once('error', reject);
    server.listen(port, '127.0.0.1', () => resolve());
  });
  return server;
}

afterEach(async () => {
  await Promise.all(temporaryDirectories.splice(0).map(directory =>
    rm(directory, { recursive: true, force: true })
  ));
});

describe('stable packaged renderer port', () => {
  it('persists the first ephemeral binding privately and reuses it', async () => {
    const userDataDirectory = await temporaryUserData();
    const first = await bindStableRendererServer({ userDataDirectory, bind: bindHttpServer });
    const firstPort = first.port;
    await first.close();

    const raw = await readFile(path.join(userDataDirectory, RENDERER_PORT_RECORD_FILENAME), 'utf8');
    expect(JSON.parse(raw)).toEqual({
      schema: RENDERER_PORT_RECORD_SCHEMA,
      host: '127.0.0.1',
      port: firstPort
    });
    const second = await bindStableRendererServer({ userDataDirectory, bind: bindHttpServer });
    expect(second.port).toBe(firstPort);
    await second.close();
  });

  it.each([
    ['corrupt JSON', '{broken'],
    ['invalid fields', JSON.stringify({ schema: RENDERER_PORT_RECORD_SCHEMA, host: '127.0.0.1', port: 0 })]
  ])('rejects a private %s record without binding', async (_label, contents) => {
    const userDataDirectory = await temporaryUserData();
    await writeFile(path.join(userDataDirectory, RENDERER_PORT_RECORD_FILENAME), contents, { mode: 0o600 });
    let binds = 0;
    await expect(bindStableRendererServer({
      userDataDirectory,
      bind: async port => { binds++; return bindHttpServer(port); }
    })).rejects.toThrow('Invalid renderer port record');
    expect(binds).toBe(0);
  });

  it('rejects a symlink or non-private saved record', async () => {
    const userDataDirectory = await temporaryUserData();
    const target = path.join(userDataDirectory, 'target.json');
    const record = JSON.stringify({ schema: RENDERER_PORT_RECORD_SCHEMA, host: '127.0.0.1', port: 54321 });
    await writeFile(target, record, { mode: 0o600 });
    await symlink(target, path.join(userDataDirectory, RENDERER_PORT_RECORD_FILENAME));
    await expect(bindStableRendererServer({ userDataDirectory, bind: bindHttpServer }))
      .rejects.toThrow('regular non-symlink');
    await rm(path.join(userDataDirectory, RENDERER_PORT_RECORD_FILENAME));
    await writeFile(path.join(userDataDirectory, RENDERER_PORT_RECORD_FILENAME), record, { mode: 0o644 });
    if (process.platform !== 'win32') {
      await chmod(path.join(userDataDirectory, RENDERER_PORT_RECORD_FILENAME), 0o644);
      await expect(bindStableRendererServer({ userDataDirectory, bind: bindHttpServer }))
        .rejects.toThrow('owner-only');
    }
  });

  it('fails closed when the saved port is occupied', async () => {
    const userDataDirectory = await temporaryUserData();
    const first = await bindStableRendererServer({ userDataDirectory, bind: bindHttpServer });
    const port = first.port;
    await first.close();
    const blocker = await occupy(port);
    try {
      await expect(bindStableRendererServer({ userDataDirectory, bind: bindHttpServer }))
        .rejects.toThrow(`Saved renderer port ${port} is already occupied`);
    } finally {
      await new Promise<void>(resolve => blocker.close(() => resolve()));
    }
  });

  it('atomically admits one first writer and closes the losing listener', async () => {
    const userDataDirectory = await temporaryUserData();
    const attemptedPorts: number[] = [];
    const capturingBind = async (port: number): Promise<BoundRendererServer> => {
      const bound = await bindHttpServer(port);
      attemptedPorts.push(bound.port);
      return bound;
    };
    const results = await Promise.allSettled([
      bindStableRendererServer({ userDataDirectory, bind: capturingBind }),
      bindStableRendererServer({ userDataDirectory, bind: capturingBind })
    ]);
    const winners = results.flatMap(result => result.status === 'fulfilled' ? [result.value] : []);
    try {
      const loser = results.find(result => result.status === 'rejected');
      expect(winners).toHaveLength(1);
      expect(loser?.status).toBe('rejected');
      if (loser?.status !== 'rejected') return;
      expect(String(loser.reason)).toContain('another GUI process selected a different renderer port');

      const saved = JSON.parse(await readFile(path.join(userDataDirectory, RENDERER_PORT_RECORD_FILENAME), 'utf8'));
      expect(attemptedPorts).toHaveLength(2);
      const losingPort = attemptedPorts.find(port => port !== saved.port);
      expect(losingPort).toBeTypeOf('number');
      const rebound = await occupy(losingPort as number);
      await new Promise<void>(resolve => rebound.close(() => resolve()));
    } finally {
      await Promise.all(winners.map(server => server.close()));
    }
  });
});
