import type { SubagentActivityRow, ToolActivityRow } from './harness-event-views';

/**
 * Fixed sentences for observed activity. They describe the recorded status of
 * an invocation and never infer a purpose or result from unfamiliar names or
 * arbitrary inputs. Shared by the Activity view and the per-turn activity
 * disclosure in the conversation so both read the same way.
 */
// Codex item types (the adapter sets `toolName` to the upstream item type).
const CODEX_ITEM_SENTENCES: Record<string, Record<ToolActivityRow['status'], string>> = {
  commandExecution: { queued: 'Command queued', permission: 'Command awaiting approval', running: 'Running command', completed: 'Command finished', failed: 'Command failed or declined' },
  fileChange: { queued: 'File change queued', permission: 'File change awaiting approval', running: 'Changing files', completed: 'File change applied', failed: 'File change failed or declined' },
  mcpToolCall: { queued: 'Tool call queued', permission: 'Tool call awaiting approval', running: 'Calling a tool', completed: 'Tool call finished', failed: 'Tool call failed' },
  dynamicToolCall: { queued: 'Tool call queued', permission: 'Tool call awaiting approval', running: 'Calling a tool', completed: 'Tool call finished', failed: 'Tool call failed' },
  webSearch: { queued: 'Web search queued', permission: 'Web search awaiting approval', running: 'Searching the web', completed: 'Web search finished', failed: 'Web search failed' },
  imageView: { queued: 'Image view queued', permission: 'Image view awaiting approval', running: 'Viewing an image', completed: 'Image viewed', failed: 'Image view failed' },
  imageGeneration: { queued: 'Image generation queued', permission: 'Image generation awaiting approval', running: 'Generating an image', completed: 'Image generated', failed: 'Image generation failed' }
};

export function actionSentence(row: Pick<ToolActivityRow, 'toolName' | 'status'>): string {
  const codex = CODEX_ITEM_SENTENCES[row.toolName];
  if (codex) return codex[row.status];
  // These two operations are defined by the registered tool descriptors. Do not
  // infer a purpose or result from an unfamiliar name or from arbitrary inputs.
  const operation = row.toolName === 'read_file' ? { verb: 'read', ongoing: 'Reading', name: 'Read' }
    : row.toolName === 'write_file' ? { verb: 'write', ongoing: 'Writing', name: 'Write' } : undefined;
  if (!operation) return {
    queued: 'Action queued', permission: 'Action permission check', running: 'Action running',
    completed: 'Action completed', failed: 'Action failed'
  }[row.status];
  return {
    queued: `Queued to ${operation.verb} file`,
    permission: `Permission check to ${operation.verb} file`,
    running: `${operation.ongoing} file`,
    // A summary can finish an invocation without establishing a file effect.
    completed: `${operation.name} action finished`,
    failed: `Failed to ${operation.verb} file`
  }[row.status];
}

export function taskSentence(row: Pick<SubagentActivityRow, 'agentName' | 'status'>): string {
  const name = row.agentName === 'subagent' ? '' : row.agentName === 'HELP_HUMAN' ? 'Assistant'
    : /^[A-Z][A-Z0-9_]*$/.test(row.agentName)
      ? row.agentName.toLowerCase().split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')
      : row.agentName;
  return `Task ${row.status}${name ? `: ${name}` : ''}`;
}

export function actionDetail(row: ToolActivityRow): string {
  return [row.toolName === 'tool' ? 'Tool name unavailable' : row.toolName, row.source, row.surface,
    `${row.eventCount} event${row.eventCount === 1 ? '' : 's'}`, row.lastEventType].filter(Boolean).join(' · ');
}
