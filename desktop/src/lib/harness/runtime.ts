import { AnthropicAgentSdkManager } from './anthropic-agent-sdk-manager';
import { StubAgentSdkManager } from './agent-sdk-manager';
import { ClaudeAgentSdkManager } from './claude-agent-sdk-manager';
import { AttachmentResolver } from './attachment-resolver';
import { hasUiApiKey } from './api-key-store';
import { PersonaComposer } from './persona-manager';
import { FileSessionManager } from './session-manager';
import { TurnEngine } from './turn-engine';
import { PiAgentEngineAdapter } from './pi-agent-engine-adapter';
import { createBoundedReadToolDefinitions } from './chirality-tool-bridge';
import { bindChiralityToolsForPi } from './pi-tool-binder';
import {
  OmlxProviderError,
  requireOmlxModel,
  resolveOmlxProviderConfig
} from './omlx-provider-config';
import {
  AgentEngineRegistry,
  LegacyAgentEngineAdapter,
  type ResolvedEngine
} from './engine-registry';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import type {
  EngineSelection,
  IAgentSdkManager,
  IAttachmentResolver,
  IPersonaManager,
  ISessionManager,
  ResolvedOpts,
  SessionRecord
} from '@chirality/runtime-contracts/types';

type HarnessRuntime = {
  sessionManager: ISessionManager;
  personaManager: IPersonaManager;
  attachmentResolver: IAttachmentResolver;
  /** @deprecated Compatibility handle for the process-default adapter. */
  agentSdkManager: IAgentSdkManager;
  engineRegistry: AgentEngineRegistry;
  resolveEngine(session: SessionRecord, opts: ResolvedOpts): ResolvedEngine;
  turnEngine: TurnEngine;
};

type HarnessRuntimeGlobal = typeof globalThis & {
  __CHIRALITY_HARNESS_RUNTIME__?: HarnessRuntime;
};

const harnessRuntimeGlobal = globalThis as HarnessRuntimeGlobal;

export type HarnessProviderMode = 'stub' | 'anthropic' | 'agentSdk';

function asNonEmptyString(value: string | undefined): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

function hasConfiguredAnthropicKey(env: NodeJS.ProcessEnv): boolean {
  return (
    hasUiApiKey() ||
    Boolean(
      asNonEmptyString(env.ANTHROPIC_API_KEY) ?? asNonEmptyString(env.CHIRALITY_ANTHROPIC_API_KEY)
    )
  );
}

export function resolveHarnessProviderMode(env: NodeJS.ProcessEnv = process.env): HarnessProviderMode {
  const raw = asNonEmptyString(env.CHIRALITY_HARNESS_PROVIDER)?.toLowerCase();

  if (raw === 'agentsdk' || raw === 'agent-sdk' || raw === 'claude-agent-sdk') {
    return 'agentSdk';
  }
  if (raw === 'anthropic') {
    return 'anthropic';
  }
  if (raw === 'stub') {
    return 'stub';
  }

  return hasConfiguredAnthropicKey(env) ? 'agentSdk' : 'stub';
}

function selectionForMode(mode: HarnessProviderMode, model: string): EngineSelection {
  if (mode === 'agentSdk') {
    return { adapterId: 'claude-agent-sdk', providerId: 'anthropic', model };
  }
  if (mode === 'anthropic') {
    return { adapterId: 'anthropic-direct', providerId: 'anthropic', model };
  }
  return { adapterId: 'stub', providerId: 'stub', model };
}

export function resolveHarnessEngineSelection(
  session: SessionRecord,
  opts: ResolvedOpts,
  env: NodeJS.ProcessEnv = process.env
): EngineSelection {
  if (session.engineSelection) {
    return {
      ...session.engineSelection,
      model: session.engineSelection.model.trim() || opts.model
    };
  }
  return selectionForMode(resolveHarnessProviderMode(env), opts.model);
}

function requireAnthropicCredential(): void {
  if (!hasConfiguredAnthropicKey(process.env)) {
    throw new HarnessError(
      'MISSING_API_KEY',
      503,
      'Anthropic API key is not configured. Enter a key in Settings or set ANTHROPIC_API_KEY.',
      { provider: 'anthropic', category: 'MISSING_API_KEY' }
    );
  }
}

function asHarnessOmlxError(error: unknown): HarnessError {
  if (!(error instanceof OmlxProviderError)) {
    return new HarnessError(
      'PROVIDER_PROTOCOL_FAILURE',
      502,
      'oMLX provider preflight failed.'
    );
  }
  if (error.code === 'OMLX_AUTHENTICATION') {
    return new HarnessError('PROVIDER_AUTH_FAILURE', 503, error.message, {
      provider: 'omlx',
      category: error.code
    });
  }
  if (error.code === 'OMLX_OFFLINE') {
    return new HarnessError('ENGINE_UNAVAILABLE', 503, error.message, {
      adapterId: 'pi',
      providerId: 'omlx',
      category: error.code
    });
  }
  if (error.code === 'OMLX_MODELS_EMPTY' || error.code === 'OMLX_MODEL_UNKNOWN') {
    return new HarnessError('MODEL_UNAVAILABLE', 503, error.message, {
      provider: 'omlx',
      category: error.code
    });
  }
  return new HarnessError(
    error.code === 'OMLX_CONFIG_INVALID' ? 'ENGINE_UNAVAILABLE' : 'PROVIDER_PROTOCOL_FAILURE',
    error.code === 'OMLX_CONFIG_INVALID' ? 503 : 502,
    error.message,
    { adapterId: 'pi', providerId: 'omlx', category: error.code }
  );
}

export function getHarnessRuntime(): HarnessRuntime {
  if (!harnessRuntimeGlobal.__CHIRALITY_HARNESS_RUNTIME__) {
    const defaultMode = resolveHarnessProviderMode();
    const sessionManager = new FileSessionManager();
    const personaManager = new PersonaComposer();
    const attachmentResolver = new AttachmentResolver();
    const managers = new Map<HarnessProviderMode, IAgentSdkManager>();

    const getManager = (mode: HarnessProviderMode): IAgentSdkManager => {
      const existing = managers.get(mode);
      if (existing) {
        return existing;
      }

      let manager: IAgentSdkManager;
      if (mode === 'anthropic') {
        manager = new AnthropicAgentSdkManager();
      } else if (mode === 'agentSdk') {
        manager = new ClaudeAgentSdkManager(undefined, async (projectRoot, persona, runtimeMode, tools) =>
          personaManager.buildSystemPrompt(projectRoot, persona, runtimeMode, tools)
        );
      } else {
        manager = new StubAgentSdkManager();
      }
      managers.set(mode, manager);
      return manager;
    };

    const engineRegistry = new AgentEngineRegistry();
    engineRegistry.register('stub', () =>
      new LegacyAgentEngineAdapter(
        {
          adapterId: 'stub',
          providerId: 'stub',
          capabilities: {
            credentials: false,
            tools: false,
            attachments: true,
            interruption: true,
            durableResume: false,
            compaction: false
          }
        },
        getManager('stub')
      )
    );
    engineRegistry.register('anthropic-direct', () =>
      new LegacyAgentEngineAdapter(
        {
          adapterId: 'anthropic-direct',
          providerId: 'anthropic',
          packageName: '@anthropic-ai/sdk',
          capabilities: {
            credentials: true,
            tools: false,
            attachments: true,
            interruption: true,
            durableResume: true,
            compaction: false
          }
        },
        getManager('anthropic'),
        requireAnthropicCredential
      )
    );
    engineRegistry.register('claude-agent-sdk', () => getManager('agentSdk') as ClaudeAgentSdkManager);
    engineRegistry.register('pi', () =>
      new PiAgentEngineAdapter({
        resolveProvider: async (input) => {
          try {
            const config = resolveOmlxProviderConfig({
              baseUrl: asNonEmptyString(process.env.CHIRALITY_OMLX_BASE_URL)
            });
            const model = await requireOmlxModel(input.opts.model, config);
            return {
              ...config,
              model: {
                id: model,
                contextWindow: 32_768,
                maxTokens: 4_096
              }
            };
          } catch (error) {
            throw asHarnessOmlxError(error);
          }
        },
        buildSystemPrompt: (input) =>
          personaManager.buildSystemPrompt(
            input.session.projectRoot,
            input.opts.persona,
            input.opts.mode,
            input.opts.tools
          ),
        resolveCustomTools: async (input) =>
          bindChiralityToolsForPi(
            createBoundedReadToolDefinitions({
              context: {
                projectRoot: input.session.projectRoot,
                sessionId: input.session.sessionId,
                turnId: input.turnId,
                mode: input.opts.mode,
                allowedReadScopes: input.session.declaredContext,
                allowedWriteTargets: []
              },
              allowedToolNames: input.opts.tools
            })
          )
      })
    );

    const resolveEngine = (session: SessionRecord, opts: ResolvedOpts): ResolvedEngine =>
      engineRegistry.resolve(resolveHarnessEngineSelection(session, opts));
    const agentSdkManager = getManager(defaultMode);

    harnessRuntimeGlobal.__CHIRALITY_HARNESS_RUNTIME__ = {
      sessionManager,
      personaManager,
      attachmentResolver,
      agentSdkManager,
      engineRegistry,
      resolveEngine,
      turnEngine: new TurnEngine({
        sessionManager,
        personaManager,
        attachmentResolver,
        resolveEngine
      })
    };
  }

  return harnessRuntimeGlobal.__CHIRALITY_HARNESS_RUNTIME__;
}

export function resetHarnessRuntimeForTests(): void {
  delete harnessRuntimeGlobal.__CHIRALITY_HARNESS_RUNTIME__;
}
