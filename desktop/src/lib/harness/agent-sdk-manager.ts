import { randomUUID } from 'node:crypto';
import { createHarnessEvent } from './event-factory';
import type { HarnessEventType } from '@chirality/runtime-contracts/event-schema';
import { HarnessError } from '@chirality/runtime-contracts/errors';
import { harnessEventToUiEvent } from './harness-ui-bridge';
import { IAgentSdkManager, ResolvedOpts, SessionRecord, UIEvent } from '@chirality/runtime-contracts/types';
import type { AgentEngineRunInput } from '@chirality/runtime-contracts/agent-engine-port';

type ActiveTurnState = {
  interrupted: boolean;
};

function delay(ms: number): Promise<void> {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

const STUB_CHUNK_DELAY_DEFAULT_MS = 35;
const STUB_POLL_DELAY_DEFAULT_MS = 50;

/**
 * Stub pacing is env-tunable so tests can compress the simulated stream
 * cadence without changing production defaults. Read at call time (not module
 * load) so a test may adjust pacing per test case.
 */
function envDelayMs(name: string, fallback: number): number {
  const raw = process.env[name];
  if (raw === undefined || raw === '') {
    return fallback;
  }
  const parsed = Number(raw);
  return Number.isFinite(parsed) && parsed >= 0 ? parsed : fallback;
}

function stubChunkDelayMs(): number {
  return envDelayMs('CHIRALITY_STUB_CHUNK_DELAY_MS', STUB_CHUNK_DELAY_DEFAULT_MS);
}

function stubPollDelayMs(): number {
  return envDelayMs('CHIRALITY_STUB_POLL_DELAY_MS', STUB_POLL_DELAY_DEFAULT_MS);
}

function chunkText(text: string, size = 24): string[] {
  const chunks: string[] = [];
  for (let index = 0; index < text.length; index += size) {
    chunks.push(text.slice(index, index + size));
  }
  return chunks.length > 0 ? chunks : ['ok'];
}

function bridgeHarnessEvent(sessionId: string, type: HarnessEventType): UIEvent | null {
  return harnessEventToUiEvent(
    createHarnessEvent({
      sessionId,
      type,
      data: { provider: 'stub-agent-sdk' }
    })
  );
}

function interruptedEvents(sessionId: string): UIEvent[] {
  const bridgedEvents = [
    bridgeHarnessEvent(sessionId, 'interruption.completed'),
    bridgeHarnessEvent(sessionId, 'turn.interrupted')
  ].filter((event): event is UIEvent => event !== null);

  return [
    ...bridgedEvents,
    {
      type: 'process:exit',
      data: {
        exitCode: 130,
        interrupted: true
      }
    }
  ];
}

const PERMISSION_DENY_MARKER = 'UNAPPROVED_DENY_TEST';
const PERMISSION_ALLOW_MARKER = 'UNAPPROVED_ALLOW_TEST';
const INTERRUPT_MARKER = 'INTERRUPT_SIGINT_TEST';
const BOOT_SDK_FAIL_MODEL_MARKER = '__BOOT_SDK_FAIL__';
const TURN_SDK_FAIL_MARKER = 'TURN_SDK_FAIL_TEST';

export class StubAgentSdkManager implements IAgentSdkManager {
  private readonly activeTurns = new Map<string, ActiveTurnState>();

  /**
   * Explicit Runtime entrypoint for the deterministic controlled adapter.
   * The stub receives the complete frozen instruction input but does not claim
   * to execute it semantically; it emits only the fixed harness simulation.
   */
  startRuntimeTurn(input: AgentEngineRunInput): AsyncIterable<UIEvent> {
    if ('instructionBasisId' in input.session && input.instructionContext === undefined) {
      throw new HarnessError(
        'ENGINE_UNAVAILABLE',
        503,
        'Controlled stub requires Runtime to supply the frozen instruction basis.'
      );
    }
    return this.startTurn(
      input.session,
      input.message,
      input.opts,
      input.contentBlocks,
      input.turnId
    );
  }

  async interrupt(sessionId: string): Promise<void> {
    const activeTurn = this.activeTurns.get(sessionId);
    if (!activeTurn) {
      throw new HarnessError('SESSION_NOT_FOUND', 404, `No active turn for session '${sessionId}'`, {
        sessionId
      });
    }

    activeTurn.interrupted = true;
  }

  async *startTurn(
    session: SessionRecord,
    message: string,
    opts: ResolvedOpts,
    _contentBlocks?: AgentEngineRunInput['contentBlocks'],
    _turnId?: string
  ): AsyncIterable<UIEvent> {
    const turnState: ActiveTurnState = { interrupted: false };
    this.activeTurns.set(session.sessionId, turnState);

    const engineSessionId = session.adapterSession?.engineSessionId ?? `stub_${randomUUID()}`;
    let fullText = message.trim();
    if (!fullText) {
      fullText = 'Turn executed successfully.';
    }

    try {
      yield {
        type: 'session:init',
        data: {
          engineSessionId,
          adapterId: 'stub',
          providerId: 'stub',
          model: opts.model
        }
      };

      if (message === 'bootstrap' && opts.model === BOOT_SDK_FAIL_MODEL_MARKER) {
        yield {
          type: 'process:exit',
          data: {
            exitCode: 1
          }
        };
        return;
      }

      if (message.includes(TURN_SDK_FAIL_MARKER)) {
        throw new HarnessError('SDK_FAILURE', 500, 'Turn failed before completion', {
          marker: TURN_SDK_FAIL_MARKER
        });
      }

      const isDontAskMode = opts.mode === 'dontAsk' || opts.mode === 'readOnly';
      if (isDontAskMode && message.includes(PERMISSION_DENY_MARKER)) {
        yield {
          type: 'tool:result',
          data: {
            name: 'bash',
            ok: false,
            output: 'permission denied'
          }
        };
        yield {
          type: 'chat:complete',
          data: {
            text: 'Denied: unapproved Bash command under dontAsk.'
          }
        };
        yield {
          type: 'session:complete',
          data: {}
        };
        yield {
          type: 'process:exit',
          data: {
            exitCode: 0
          }
        };
        return;
      }

      if (isDontAskMode && message.includes(PERMISSION_ALLOW_MARKER)) {
        yield {
          type: 'tool:result',
          data: {
            name: 'bash',
            ok: true,
            output: PERMISSION_ALLOW_MARKER
          }
        };
      }

      // Test marker: keep the turn open while bundle-boundary interrupt verification imports routes.
      if (message.includes(INTERRUPT_MARKER)) {
        const deadline = Date.now() + 4_500;
        while (!turnState.interrupted && Date.now() < deadline) {
          await delay(stubPollDelayMs());
        }
      }

      const chunks = chunkText(fullText);
      let combined = '';

      for (const chunk of chunks) {
        if (turnState.interrupted) {
          yield* interruptedEvents(session.sessionId);
          return;
        }

        combined += chunk;
        yield {
          type: 'chat:delta',
          data: {
            text: chunk
          }
        };

        await delay(stubChunkDelayMs());
      }

      if (turnState.interrupted) {
        yield* interruptedEvents(session.sessionId);
        return;
      }

      yield {
        type: 'chat:complete',
        data: {
          text: combined
        }
      };

      yield {
        type: 'session:complete',
        data: {}
      };

      yield {
        type: 'process:exit',
        data: {
          exitCode: 0
        }
      };
    } finally {
      this.activeTurns.delete(session.sessionId);
    }
  }
}
