import { randomUUID } from 'node:crypto';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import type {
  DaemonHarnessPort,
  HostedBootstrapPort
} from '../../../lib/runtime-client/daemon-harness-port';
import { listAgentRoster, selectDirectChatPersonas, assertDirectChatPersona } from '../../../lib/harness/agent-roster';
import { getPermissionBroker } from '../../../lib/harness/permission-broker';
import { resolveRuntimeOptions } from '../../../lib/harness/options';
import { getHarnessRuntime } from '../../../lib/harness/runtime';
import { buildHarnessRuntimeFingerprint } from '../../../lib/harness/runtime-fingerprint';
import { scaffoldExecutionRoot } from '../../../lib/harness/scaffold';
import { replayHarnessEvents } from '../../../lib/harness/session-events';
import { assertProjectRootAccessible } from '../../../lib/harness/session-manager';
import { deriveTranscriptView } from '@chirality/runtime-contracts/transcript-replay';
import { CHAT_SECTION } from '../../../lib/shell/loop-first';
import { CHIRALITY_ROLES } from '@chirality/runtime-contracts/v3';

/**
 * Hermetic daemon-port fixture for the pre-existing route contract suite. It
 * deliberately lives in tests: production routes cannot import or fall back to
 * the in-process harness. The underlying harness supplies realistic session,
 * replay, interruption, and streaming behavior while the tests exercise only
 * the injected daemon boundary.
 */
export function createFakeDaemonHarnessPort(): DaemonHarnessPort {
  return {
    async createSession(request) {
      const persona = request.persona?.trim() ?? '';
      if (request.mode === CHAT_SECTION && persona) {
        await assertDirectChatPersona(persona);
      }
      const session = await getHarnessRuntime().sessionManager.create(request);
      return { session };
    },

    async listSessions(projectRoot) {
      return { sessions: await getHarnessRuntime().sessionManager.list(projectRoot) };
    },

    async getSession(sessionId) {
      return { session: await getHarnessRuntime().sessionManager.getById(sessionId) };
    },

    async deleteSession(sessionId) {
      await getHarnessRuntime().sessionManager.delete(sessionId);
      return { ok: true };
    },

    async bootSession(request) {
      const runtime = getHarnessRuntime();
      const session = await runtime.sessionManager.resume(request.sessionId);
      await assertProjectRootAccessible(session.projectRoot);
      const resolvedOpts = await resolveRuntimeOptions(session, request.opts);
      await runtime.personaManager.buildSystemPrompt(
        session.projectRoot,
        resolvedOpts.persona,
        resolvedOpts.mode,
        resolvedOpts.tools
      );
      const bootFingerprint = runtime.personaManager.getBootFingerprint(
        resolvedOpts.persona,
        resolvedOpts.mode,
        session.projectRoot,
        resolvedOpts.tools
      );
      const engine = runtime.resolveEngine(session, resolvedOpts);
      const effectiveOpts = engine.selection.model
        ? { ...resolvedOpts, model: engine.selection.model }
        : resolvedOpts;
      const runInput = {
        session,
        message: 'bootstrap',
        opts: effectiveOpts,
        turnId: `turn_${randomUUID()}`
      };
      await engine.port.preflight(runInput);

      let engineSessionId = session.adapterSession?.engineSessionId ?? session.engineSessionId;
      let adapterId = engine.selection.adapterId;
      let providerId = engine.selection.providerId;
      let model = effectiveOpts.model;
      let claudeSessionId =
        providerId === 'anthropic' ? session.claudeSessionId : undefined;

      for await (const event of engine.port.startTurn(runInput)) {
        if (event.type === 'session:init') {
          engineSessionId = event.data.engineSessionId;
          adapterId = event.data.adapterId;
          providerId = event.data.providerId;
          model = event.data.model;
          claudeSessionId =
            providerId === 'anthropic' ? event.data.claudeSessionId : undefined;
        }
        if (event.type === 'process:exit' && event.data.exitCode !== 0) {
          throw new HarnessError('SDK_FAILURE', 500, 'Boot turn failed before completion', {
            exitCode: event.data.exitCode
          });
        }
      }

      if (!engineSessionId) {
        throw new HarnessError(
          'SDK_FAILURE',
          500,
          'Boot turn did not initialize an engine session'
        );
      }

      const bootedAt = new Date().toISOString();
      const runtimeFingerprint = buildHarnessRuntimeFingerprint(engine.port.descriptor, {
        adapterId,
        providerId,
        model
      });
      const updatedSession = await runtime.sessionManager.save(request.sessionId, {
        engineSessionId,
        engineSelection: { adapterId, providerId, model },
        adapterSession: {
          ...session.adapterSession,
          engineSessionId,
          packageName: engine.port.descriptor.packageName,
          packageVersion: engine.port.descriptor.packageVersion
        },
        ...(providerId === 'anthropic' ? { claudeSessionId } : {}),
        ...(adapterId === 'claude-agent-sdk'
          ? {
              sdkSessionId: engineSessionId,
              sdkPackageVersion: engine.port.descriptor.packageVersion
            }
          : {}),
        bootFingerprint,
        runtimeFingerprint,
        bootedAt,
        model
      });

      return {
        session: updatedSession,
        boot: {
          engineSessionId,
          adapterId,
          providerId,
          model,
          ...(providerId === 'anthropic' && claudeSessionId ? { claudeSessionId } : {}),
          bootFingerprint,
          runtimeFingerprint,
          bootedAt
        }
      };
    },

    async replaySession(sessionId) {
      const session = await getHarnessRuntime().sessionManager.getById(sessionId);
      const replay = await replayHarnessEvents(sessionId);
      return {
        ...replay,
        session,
        transcript: deriveTranscriptView(replay.events, session),
        instructionHistory: [],
        instructionBases: []
      };
    },

    async turn(request) {
      return getHarnessRuntime().turnEngine.runTurn(request);
    },

    async attachTurn() {
      throw new HarnessError('SESSION_NOT_FOUND', 404, 'No active or retained turn in fake daemon', { reason: 'TURN_NOT_ACTIVE' });
    },

    async turnState() {
      return { active: false, lastSeq: 0 };
    },

    async listRequests() {
      return { requests: [] };
    },

    async answerRequest() {
      throw new HarnessError('ENGINE_UNAVAILABLE', 503, 'Server request answers are not configured in fake daemon');
    },

    async steerReceipt(_sessionId, request) { return { operationId: request.operationId, turnId: request.expectedTurnId, status: 'unknown', message: 'No native receipt fixture.' }; },
    async steer(_sessionId, request) { return { operationId: request.operationId, turnId: request.expectedTurnId, status: 'rejected', message: 'Test port has no native steering supplier.' }; },
    async interrupt(request) {
      getPermissionBroker().clearSession(request.sessionId, 'deny');
      await getHarnessRuntime().turnEngine.interrupt(request.sessionId);
      return { ok: true };
    },

    async decidePermission(request) {
      return {
        ok: true,
        decided: getPermissionBroker().decide(request)
      };
    },

    async listAgents(request) {
      const roster = await listAgentRoster();
      return {
        agents: request.directChatOnly ? selectDirectChatPersonas(roster) : roster
      };
    },

    async listRoles() {
      return { schemaVersion: 'chirality.roles/v3', defaultRole: 'HELP_HUMAN', roles: CHIRALITY_ROLES };
    },

    async listMethods() {
      return { schemaVersion: 'chirality.methods/v3', methods: [], malformedPackages: [] };
    },

    async inspectMethod() {
      throw new HarnessError('INVALID_REQUEST', 404, 'Method not found in fake daemon');
    },

    async resolveSelectedContext() {
      throw new HarnessError('ENGINE_UNAVAILABLE', 503, 'Selected context is not configured in fake daemon');
    },

    async replaceSelectedMethods() {
      throw new HarnessError('ENGINE_UNAVAILABLE', 503, 'Method replacement is not configured in fake daemon');
    },

    async getNativePlanCapability() {
      return {
        schemaVersion: 'chirality.native-plan-capability/v3',
        status: 'unavailable',
        reason: 'Fake daemon has no qualified native Plan adapter'
      };
    },

    async listNativePlanRevisions() {
      return {
        schemaVersion: 'chirality.native-plan-revisions/v3',
        status: 'unavailable',
        reason: 'Fake daemon has no qualified native Plan adapter',
        revisions: []
      };
    },

    async listNativePlanClarifications() {
      return {
        schemaVersion: 'chirality.native-plan-clarifications/v3',
        status: 'unavailable',
        reason: 'Fake daemon has no qualified native Plan adapter',
        clarifications: []
      };
    },

    async replyNativePlanClarification() {
      throw new HarnessError('ENGINE_UNAVAILABLE', 503, 'Native Plan clarification reply is not configured in fake daemon');
    },

    async exportNativePlan() {
      throw new HarnessError('ENGINE_UNAVAILABLE', 503, 'Native Plan export is not configured in fake daemon');
    },

    async scaffold(request) {
      return scaffoldExecutionRoot(request);
    }
  };
}

export function createFakeHostedBootstrapPort(): HostedBootstrapPort {
  return {
    async bindProject() {
      return { registration: 'required' };
    },
    async getStatus() {
      return { registration: 'required' };
    },
    async initializeProject() {
      throw new HarnessError(
        'ENGINE_UNAVAILABLE',
        503,
        'Hosted project initialization is not configured in fake daemon'
      );
    },
    async grantProviderNetworkConsent() {
      throw new HarnessError(
        'ENGINE_UNAVAILABLE',
        503,
        'Hosted provider consent is not configured in fake daemon'
      );
    },
    async startLogin() {
      throw new HarnessError(
        'ENGINE_UNAVAILABLE',
        503,
        'Hosted login is not configured in fake daemon'
      );
    },
    async cancelLogin() {
      throw new HarnessError(
        'ENGINE_UNAVAILABLE',
        503,
        'Hosted login cancellation is not configured in fake daemon'
      );
    },
    async signOut() {
      throw new HarnessError(
        'ENGINE_UNAVAILABLE',
        503,
        'Hosted project sign-out is not configured in fake daemon'
      );
    }
  };
}
