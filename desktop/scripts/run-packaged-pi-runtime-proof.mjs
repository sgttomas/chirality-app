#!/usr/bin/env node

import { spawn } from 'node:child_process';
import { createServer } from 'node:http';
import { mkdir, mkdtemp, readFile, readdir, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';

function memoryCredentialStore() {
  const values = new Map();
  return {
    async read(providerId) { return values.get(providerId); },
    async list() { return []; },
    async modify(providerId, fn) {
      const next = await fn(values.get(providerId));
      if (next !== undefined) values.set(providerId, next);
      return values.get(providerId);
    },
    async delete(providerId) { values.delete(providerId); }
  };
}

function memoryModelsStore() {
  const values = new Map();
  return {
    async read(providerId) { return values.get(providerId); },
    async write(providerId, value) { values.set(providerId, value); },
    async delete(providerId) { values.delete(providerId); }
  };
}

function sse(response, chunks) {
  response.writeHead(200, {
    'content-type': 'text/event-stream',
    'cache-control': 'no-cache',
    connection: 'keep-alive'
  });
  for (const chunk of chunks) response.write(`data: ${JSON.stringify(chunk)}\n\n`);
  response.end('data: [DONE]\n\n');
}

function completionChunk(model, delta, finishReason = null) {
  return {
    id: 'chatcmpl_packaged_pi_proof',
    object: 'chat.completion.chunk',
    created: 1,
    model,
    choices: [{ index: 0, delta, finish_reason: finishReason }]
  };
}

async function readEvidenceTree(root) {
  const chunks = [];
  for (const entry of await readdir(root, { withFileTypes: true })) {
    const absolutePath = path.join(root, entry.name);
    if (entry.isDirectory()) {
      chunks.push(await readEvidenceTree(absolutePath));
    } else if (entry.isFile()) {
      chunks.push(await readFile(absolutePath, 'utf8').catch(() => ''));
    }
  }
  return chunks.join('\n');
}

async function runLegacyAssetChild() {
  const piPackageUrl = process.env.CHIRALITY_PACKAGED_PI_URL;
  const projectRoot = process.env.CHIRALITY_PACKAGED_PI_PROJECT;
  if (!piPackageUrl || !projectRoot) throw new Error('Packaged Pi child environment is incomplete');

  const apiKey = 'packaged-pi-proof-key';
  const modelId = 'packaged-pi-proof-model';
  const requests = [];
  const server = createServer(async (request, response) => {
    const body = [];
    for await (const chunk of request) body.push(chunk);
    const parsed = body.length > 0 ? JSON.parse(Buffer.concat(body).toString('utf8')) : {};
    requests.push({
      method: request.method,
      url: request.url,
      authorized: request.headers.authorization === `Bearer ${apiKey}`,
      body: parsed
    });
    if (request.url !== '/v1/chat/completions' || request.method !== 'POST') {
      response.writeHead(404).end();
      return;
    }
    if (request.headers.authorization !== `Bearer ${apiKey}`) {
      response.writeHead(401, { 'content-type': 'application/json' });
      response.end(JSON.stringify({ error: { message: 'unauthorized' } }));
      return;
    }
    if (requests.length === 1) {
      sse(response, [
        completionChunk(modelId, { role: 'assistant', content: '' }),
        completionChunk(modelId, {
          tool_calls: [{
            index: 0,
            id: 'call_packaged_read',
            type: 'function',
            function: {
              name: 'read_file',
              arguments: '{"file_path":"fixture.txt"}'
            }
          }]
        }),
        completionChunk(modelId, {}, 'tool_calls')
      ]);
      return;
    }
    sse(response, [
      completionChunk(modelId, { role: 'assistant', content: '' }),
      completionChunk(modelId, { content: 'PACKAGED_PI_PROOF_OK' }),
      completionChunk(modelId, {}, 'stop')
    ]);
  });
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });

  let session;
  try {
    const address = server.address();
    if (!address || typeof address === 'string') throw new Error('Fake provider has no TCP address');
    const pi = await import(piPackageUrl);
    const modelRuntime = await pi.ModelRuntime.create({
      credentials: memoryCredentialStore(),
      modelsPath: null,
      modelsStore: memoryModelsStore(),
      allowModelNetwork: false
    });
    modelRuntime.registerProvider('omlx', {
      baseUrl: `http://127.0.0.1:${address.port}/v1`,
      api: 'openai-completions',
      models: [{
        id: modelId,
        name: modelId,
        reasoning: false,
        input: ['text'],
        cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
        contextWindow: 32768,
        maxTokens: 4096
      }]
    });
    await modelRuntime.setRuntimeApiKey('omlx', apiKey);
    const model = modelRuntime.getModel('omlx', modelId);
    if (!model) throw new Error('Packaged Pi did not construct the fake model');
    const resourceLoader = new pi.DefaultResourceLoader({
      cwd: projectRoot,
      agentDir: path.join(projectRoot, '.ambient-disabled'),
      settingsManager: pi.SettingsManager.inMemory({}, { projectTrusted: false }),
      noExtensions: true,
      noSkills: true,
      noPromptTemplates: true,
      noThemes: true,
      noContextFiles: true,
      systemPrompt: 'Use only the supplied read_file tool.',
      extensionsOverride: (base) => ({ ...base, extensions: [], errors: [] }),
      skillsOverride: () => ({ skills: [], diagnostics: [] }),
      promptsOverride: () => ({ prompts: [], diagnostics: [] }),
      themesOverride: () => ({ themes: [], diagnostics: [] }),
      agentsFilesOverride: () => ({ agentsFiles: [] }),
      appendSystemPromptOverride: () => []
    });
    await resourceLoader.reload();
    const toolCalls = [];
    const readTool = {
      name: 'read_file',
      label: 'Read File',
      description: 'Read the packaged proof fixture.',
      parameters: {
        type: 'object',
        additionalProperties: false,
        required: ['file_path'],
        properties: { file_path: { type: 'string' } }
      },
      async execute(toolUseId, params) {
        toolCalls.push({ toolUseId, params });
        if (params.file_path !== 'fixture.txt') throw new Error('Unexpected proof path');
        const text = await readFile(path.join(projectRoot, 'fixture.txt'), 'utf8');
        return { content: [{ type: 'text', text }], details: { source: 'packaged-proof' } };
      }
    };
    const created = await pi.createAgentSession({
      cwd: projectRoot,
      model,
      modelRuntime,
      sessionManager: pi.SessionManager.inMemory(projectRoot, { id: 'packaged_pi_proof' }),
      settingsManager: pi.SettingsManager.inMemory(
        { defaultProvider: 'omlx', defaultModel: modelId, packages: [], extensions: [], skills: [], prompts: [], themes: [] },
        { projectTrusted: false }
      ),
      resourceLoader,
      noTools: 'all',
      tools: ['read_file'],
      customTools: [readTool]
    });
    session = created.session;
    let assistantText = '';
    session.subscribe((event) => {
      if (event.type !== 'message_end' || event.message?.role !== 'assistant') return;
      assistantText = event.message.content
        .filter((block) => block.type === 'text')
        .map((block) => block.text)
        .join('');
    });
    await session.prompt('Read fixture.txt, then report PACKAGED_PI_PROOF_OK.', {
      expandPromptTemplates: false
    });
    await session.waitForIdle();
    const secondMessages = requests[1]?.body?.messages ?? [];
    const result = {
      status: assistantText.includes('PACKAGED_PI_PROOF_OK') ? 'PASS' : 'FAIL',
      packageVersion: pi.VERSION,
      activeTools: session.getActiveToolNames(),
      toolCalls,
      requestCount: requests.length,
      requestsAuthorized: requests.every((entry) => entry.authorized),
      toolResultReturned: secondMessages.some(
        (message) => message.role === 'tool' && String(message.content).includes('KNOWN_PACKAGED_FIXTURE')
      ),
      assistantText
    };
    process.stdout.write(`${JSON.stringify(result)}\n`);
    if (result.status !== 'PASS') process.exitCode = 1;
  } finally {
    session?.dispose();
    await new Promise((resolve) => server.close(resolve));
  }
}

async function runChild() {
  const turnRoutePath = process.env.CHIRALITY_PACKAGED_TURN_ROUTE;
  const projectRoot = process.env.CHIRALITY_PACKAGED_PI_PROJECT;
  if (!turnRoutePath || !projectRoot) {
    throw new Error('Packaged production-route proof environment is incomplete');
  }

  const apiKey = 'packaged-pi-proof-key';
  const modelId = 'packaged-pi-proof-model';
  const sessionId = 'sess_packaged_pi_child';
  const sessionRoot = path.join(projectRoot, '.chirality', 'sessions');
  const requests = [];
  let completionCount = 0;
  const server = createServer(async (request, response) => {
    const body = [];
    for await (const chunk of request) body.push(chunk);
    const parsed = body.length > 0 ? JSON.parse(Buffer.concat(body).toString('utf8')) : {};
    requests.push({
      method: request.method,
      url: request.url,
      authorized: request.headers.authorization === `Bearer ${apiKey}`,
      body: parsed
    });
    if (request.headers.authorization !== `Bearer ${apiKey}`) {
      response.writeHead(401, { 'content-type': 'application/json' });
      response.end(JSON.stringify({ error: { message: 'unauthorized' } }));
      return;
    }
    if (request.url === '/v1/models' && request.method === 'GET') {
      response.writeHead(200, { 'content-type': 'application/json' });
      response.end(JSON.stringify({ data: [{ id: modelId, object: 'model' }] }));
      return;
    }
    if (request.url !== '/v1/chat/completions' || request.method !== 'POST') {
      response.writeHead(404).end();
      return;
    }
    completionCount += 1;
    if (completionCount === 1) {
      sse(response, [
        completionChunk(modelId, { role: 'assistant', content: '' }),
        completionChunk(modelId, {
          tool_calls: [{
            index: 0,
            id: 'call_packaged_read',
            type: 'function',
            function: { name: 'read_file', arguments: '{"file_path":"fixture.txt"}' }
          }]
        }),
        completionChunk(modelId, {}, 'tool_calls')
      ]);
      return;
    }
    sse(response, [
      completionChunk(modelId, { role: 'assistant', content: '' }),
      completionChunk(modelId, { content: 'PACKAGED_PI_PROOF_OK' }),
      completionChunk(modelId, {}, 'stop')
    ]);
  });
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });

  try {
    const address = server.address();
    if (!address || typeof address === 'string') throw new Error('Fake provider has no TCP address');
    process.env.CHIRALITY_SESSION_ROOT = sessionRoot;
    process.env.CHIRALITY_OMLX_API_KEY = apiKey;
    process.env.CHIRALITY_OMLX_BASE_URL = `http://127.0.0.1:${address.port}/v1`;
    const now = new Date().toISOString();
    const session = {
      sessionId,
      projectRoot,
      persona: 'TASK',
      mode: 'readOnly',
      createdAt: now,
      updatedAt: now,
      model: modelId,
      engineSelection: { adapterId: 'pi', providerId: 'omlx', model: modelId },
      agentType: 2,
      parentSessionId: 'sess_packaged_claude_parent',
      approvalRef: 'PACKAGED-PROOF-APPROVAL',
      declaredContext: [projectRoot],
      declaredTools: ['read_file'],
      allowedWriteTargets: []
    };
    const sessionDirectory = path.join(sessionRoot, sessionId);
    await mkdir(sessionDirectory, { recursive: true });
    await writeFile(path.join(sessionDirectory, 'session.json'), `${JSON.stringify(session, null, 2)}\n`);

    const packagedRequire = createRequire(import.meta.url);
    const route = packagedRequire(turnRoutePath);
    const response = await route.routeModule.userland.POST(
      new Request('http://127.0.0.1/api/harness/turn', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          sessionId,
          message: 'Read fixture.txt, then report PACKAGED_PI_PROOF_OK.',
          opts: {
            model: modelId,
            persona: 'TASK',
            mode: 'readOnly',
            tools: ['read_file']
          }
        })
      })
    );
    const streamText = await response.text();
    if (response.status !== 200) {
      process.stdout.write(`PACKAGED_PI_RESULT=${JSON.stringify({
        status: 'FAIL',
        proofBoundary: 'packaged-production-route-registry-adapter-provider-tool-persistence',
        responseStatus: response.status,
        responseBody: streamText.slice(0, 4_000),
        requestCount: requests.length,
        requestsAuthorized: requests.every((entry) => entry.authorized)
      })}\n`);
      process.exitCode = 1;
      return;
    }
    const uiEvents = streamText
      .trim()
      .split('\n\n')
      .filter(Boolean)
      .map((block) => {
        const lines = block.split('\n');
        const eventLine = lines.find((line) => line.startsWith('event: '));
        const dataLine = lines.find((line) => line.startsWith('data: '));
        if (!eventLine || !dataLine) {
          throw new Error(`Malformed packaged SSE block: ${block.slice(0, 200)}`);
        }
        return {
          type: eventLine.slice('event: '.length),
          data: JSON.parse(dataLine.slice('data: '.length))
        };
      });
    const eventFile = path.join(sessionDirectory, 'events.jsonl');
    const persistedText = await readFile(eventFile, 'utf8');
    const allEvidenceText = await readEvidenceTree(sessionDirectory);
    const updatedSession = JSON.parse(
      await readFile(path.join(sessionDirectory, 'session.json'), 'utf8')
    );
    const persisted = persistedText.trim().split('\n').filter(Boolean).map((line) => JSON.parse(line));
    const persistedTypes = persisted.map((event) => event.type);
    const result = {
      status:
        response.status === 200 &&
        uiEvents.some((event) => event.type === 'session:init' && event.data?.adapterId === 'pi' && event.data?.providerId === 'omlx' && event.data?.model === modelId) &&
        uiEvents.some((event) => event.type === 'chat:complete' && String(event.data?.text).includes('PACKAGED_PI_PROOF_OK')) &&
        uiEvents.at(-1)?.type === 'process:exit' &&
        uiEvents.at(-1)?.data?.exitCode === 0 &&
        persistedTypes.includes('message.accepted') &&
        persistedTypes.includes('tool.permission') &&
        persistedTypes.includes('tool.started') &&
        persistedTypes.includes('tool.completed') &&
        persistedTypes.includes('turn.completed') &&
        updatedSession.engineSelection?.adapterId === 'pi' &&
        updatedSession.engineSelection?.providerId === 'omlx' &&
        updatedSession.engineSelection?.model === modelId &&
        updatedSession.adapterSession?.packageVersion === '0.82.0' &&
        !allEvidenceText.includes('KNOWN_PACKAGED_FIXTURE') &&
        !allEvidenceText.includes(apiKey)
          ? 'PASS'
          : 'FAIL',
      proofBoundary: 'packaged-production-route-registry-adapter-provider-tool-persistence',
      responseStatus: response.status,
      uiEventTypes: uiEvents.map((event) => event.type),
      persistedTypes,
      engineSelection: updatedSession.engineSelection,
      adapterPackageVersion: updatedSession.adapterSession?.packageVersion,
      requestCount: requests.length,
      modelDiscoveryCount: requests.filter((entry) => entry.url === '/v1/models').length,
      completionCount,
      requestsAuthorized: requests.every((entry) => entry.authorized),
      rawFixtureAbsentFromEvidence: !allEvidenceText.includes('KNOWN_PACKAGED_FIXTURE'),
      credentialAbsentFromEvidence: !allEvidenceText.includes(apiKey)
    };
    process.stdout.write(`PACKAGED_PI_RESULT=${JSON.stringify(result)}\n`);
    if (result.status !== 'PASS') process.exitCode = 1;
  } finally {
    await new Promise((resolve) => server.close(resolve));
  }
}

async function runParent() {
  const frontendRoot = process.cwd();
  const resourcesRoot = path.resolve(
    process.env.CHIRALITY_PACKAGED_RESOURCES_ROOT ??
      path.join(frontendRoot, 'dist/mac-arm64/Chirality.app/Contents/Resources')
  );
  const electronBinary = path.resolve(
    process.env.CHIRALITY_PACKAGED_ELECTRON ??
      path.join(resourcesRoot, '../MacOS/Chirality')
  );
  const packageEntry = path.join(
    resourcesRoot,
    'app.asar/node_modules/@earendil-works/pi-coding-agent/dist/index.js'
  );
  const tempRoot = await mkdtemp(path.join(os.tmpdir(), 'chirality-packaged-pi-proof-'));
  const projectRoot = path.join(tempRoot, 'project');
  const outputRoot = path.join(frontendRoot, 'artifacts/harness/packaged-pi/latest');
  await mkdir(projectRoot, { recursive: true });
  await mkdir(outputRoot, { recursive: true });
  await writeFile(path.join(projectRoot, 'fixture.txt'), 'KNOWN_PACKAGED_FIXTURE\n', 'utf8');

  const child = spawn(electronBinary, [new URL(import.meta.url).pathname, '--legacy-asset-child'], {
    env: {
      ...process.env,
      ELECTRON_RUN_AS_NODE: '1',
      CHIRALITY_PACKAGED_PI_URL: pathToFileURL(packageEntry).href,
      CHIRALITY_PACKAGED_PI_PROJECT: projectRoot
    },
    stdio: ['ignore', 'pipe', 'pipe']
  });
  let stdout = '';
  let stderr = '';
  child.stdout.setEncoding('utf8');
  child.stderr.setEncoding('utf8');
  child.stdout.on('data', (chunk) => { stdout += chunk; });
  child.stderr.on('data', (chunk) => { stderr += chunk; });
  const exitCode = await new Promise((resolve, reject) => {
    child.once('error', reject);
    child.once('exit', (code) => resolve(code ?? 1));
  });
  const resultLine = stdout.trim().split('\n').findLast(Boolean);
  const childResult = resultLine ? JSON.parse(resultLine) : null;
  const summary = {
    status:
      exitCode === 0 &&
      childResult?.status === 'PASS' &&
      childResult?.packageVersion === '0.82.0' &&
      childResult?.activeTools?.length === 1 &&
      childResult?.activeTools?.[0] === 'read_file' &&
      childResult?.toolCalls?.length === 1 &&
      childResult?.requestCount === 2 &&
      childResult?.requestsAuthorized === true &&
      childResult?.toolResultReturned === true
        ? 'PASS'
        : 'FAIL',
    proof: 'offline-packaged-pi-sdk-fake-loopback-read-tool',
    exitCode,
    resourcesRoot,
    packageEntry,
    child: childResult,
    stderr: stderr.trim()
  };
  await writeFile(path.join(outputRoot, 'summary.json'), `${JSON.stringify(summary, null, 2)}\n`, 'utf8');
  console.log(`packaged Pi runtime proof status: ${summary.status.toLowerCase()}`);
  if (summary.status !== 'PASS') {
    if (summary.stderr) console.error(summary.stderr);
    process.exitCode = 1;
  }
}

if (process.argv.includes('--legacy-asset-child')) {
  try {
    await runLegacyAssetChild();
  } catch (error) {
    process.stdout.write(`${JSON.stringify({
      status: 'FAIL',
      errorName: error instanceof Error ? error.name : 'UnknownError',
      errorMessage: error instanceof Error ? error.message.slice(0, 2_000) : 'Packaged child failed'
    })}\n`);
    process.exitCode = 1;
  }
} else if (process.argv.includes('--child')) {
  try {
    await runChild();
  } catch (error) {
    process.stdout.write(`PACKAGED_PI_RESULT=${JSON.stringify({
      status: 'FAIL',
      proofBoundary: 'packaged-production-route-registry-adapter-provider-tool-persistence',
      errorName: error instanceof Error ? error.name : 'UnknownError',
      errorMessage: error instanceof Error ? error.message.slice(0, 2_000) : 'Packaged child failed'
    })}\n`);
    process.exitCode = 1;
  }
} else {
  await runParent();
}
