import type { SDKMessage, SpawnedProcess, SpawnOptions } from '@anthropic-ai/claude-agent-sdk';
import { EventEmitter } from 'node:events';
import { PassThrough, Writable } from 'node:stream';

export const SCRIPTED_AGENT_SDK_PROOF_ENV = 'CHIRALITY_AGENTSDK_SCRIPTED_PROOF';

class ScriptedAgentSdkProofProcess extends EventEmitter implements SpawnedProcess {
  readonly stdout = new PassThrough();
  readonly stdin = new Writable({
    write(_chunk, _encoding, callback): void {
      callback();
    }
  });

  killed = false;
  exitCode: number | null = null;

  kill(signal: NodeJS.Signals): boolean {
    if (this.exitCode !== null) {
      return false;
    }
    this.killed = true;
    this.exitCode = signal === 'SIGTERM' || signal === 'SIGINT' ? 130 : 1;
    this.stdout.end();
    this.emit('exit', null, signal);
    return true;
  }

  writeMessage(message: SDKMessage): void {
    this.stdout.write(`${JSON.stringify(message)}\n`);
  }

  finish(): void {
    if (this.exitCode !== null) {
      return;
    }
    this.exitCode = 0;
    this.stdout.end();
    this.emit('exit', 0, null);
  }
}

function sdkMessage(message: SDKMessage): SDKMessage {
  return message;
}

function scriptedMessages(options: SpawnOptions): SDKMessage[] {
  return [
    sdkMessage({
      type: 'system',
      subtype: 'init',
      session_id: 'sdk_network_proof_1',
      uuid: '00000000-0000-0000-0000-000000000201',
      apiKeySource: 'temporary',
      claude_code_version: '2.1.150',
      cwd: options.cwd ?? '',
      tools: [],
      mcp_servers: [],
      model: 'claude-test',
      permissionMode: 'default',
      slash_commands: [],
      output_style: 'default',
      skills: [],
      plugins: []
    }),
    sdkMessage({
      type: 'stream_event',
      event: {
        type: 'content_block_delta',
        index: 0,
        delta: {
          type: 'text_delta',
          text: 'scripted agentSdk network proof'
        }
      },
      parent_tool_use_id: null,
      uuid: '00000000-0000-0000-0000-000000000202',
      session_id: 'sdk_network_proof_1'
    }),
    sdkMessage({
      type: 'result',
      subtype: 'success',
      duration_ms: 10,
      duration_api_ms: 0,
      is_error: false,
      num_turns: 1,
      result: 'scripted agentSdk network proof',
      stop_reason: 'end_turn',
      total_cost_usd: 0,
      usage: {} as never,
      modelUsage: {},
      permission_denials: [],
      uuid: '00000000-0000-0000-0000-000000000203',
      session_id: 'sdk_network_proof_1'
    })
  ];
}

function shouldUseScriptedAgentSdkProof(env: NodeJS.ProcessEnv = process.env): boolean {
  return (
    env[SCRIPTED_AGENT_SDK_PROOF_ENV] === '1' &&
    (env.NODE_ENV === 'development' || env.NODE_ENV === 'test')
  );
}

export function createScriptedAgentSdkProofSpawn(
  env: NodeJS.ProcessEnv = process.env
): ((options: SpawnOptions) => SpawnedProcess) | undefined {
  if (!shouldUseScriptedAgentSdkProof(env)) {
    return undefined;
  }

  return (options: SpawnOptions): SpawnedProcess => {
    const process = new ScriptedAgentSdkProofProcess();
    const abortListener = (): void => {
      process.kill('SIGTERM');
    };
    options.signal.addEventListener('abort', abortListener, { once: true });

    queueMicrotask(() => {
      if (process.exitCode !== null) {
        return;
      }
      for (const message of scriptedMessages(options)) {
        process.writeMessage(message);
      }
      options.signal.removeEventListener('abort', abortListener);
      process.finish();
    });

    return process;
  };
}
