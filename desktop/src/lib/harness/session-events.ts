import { mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { HarnessEvent } from '@chirality/runtime-contracts/event-schema';
import { redactJsonLike } from './run-logger';

function getSessionRootDirectory(): string {
  return process.env.CHIRALITY_SESSION_ROOT ?? path.join(process.cwd(), '.chirality', 'sessions');
}

function getSessionEventFilePath(sessionId: string): string {
  return path.join(getSessionRootDirectory(), sessionId, 'events.jsonl');
}

export async function appendHarnessEvent(event: HarnessEvent): Promise<string> {
  const filePath = getSessionEventFilePath(event.sessionId);
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, `${JSON.stringify(redactJsonLike(event))}\n`, {
    encoding: 'utf8',
    flag: 'a'
  });
  return filePath;
}

export type HarnessReplaySummary = {
  eventCount: number;
  malformedLineCount: number;
  eventTypeCounts: Record<string, number>;
  firstTimestamp?: string;
  lastTimestamp?: string;
};

function summarizeReplayedEvents(
  events: readonly HarnessEvent[],
  malformedLineCount: number
): HarnessReplaySummary {
  const eventTypeCounts: Record<string, number> = {};
  for (const event of events) {
    eventTypeCounts[event.type] = (eventTypeCounts[event.type] ?? 0) + 1;
  }

  return {
    eventCount: events.length,
    malformedLineCount,
    eventTypeCounts,
    firstTimestamp: events[0]?.timestamp,
    lastTimestamp: events.length > 0 ? events[events.length - 1].timestamp : undefined
  };
}

export async function replayHarnessEvents(sessionId: string): Promise<{
  events: HarnessEvent[];
  malformedLineCount: number;
  summary: HarnessReplaySummary;
}> {
  const filePath = getSessionEventFilePath(sessionId);
  let raw = '';
  try {
    raw = await readFile(filePath, 'utf8');
  } catch {
    return {
      events: [],
      malformedLineCount: 0,
      summary: summarizeReplayedEvents([], 0)
    };
  }

  const events: HarnessEvent[] = [];
  let malformedLineCount = 0;
  for (const line of raw.split('\n')) {
    if (line.trim().length === 0) {
      continue;
    }
    try {
      events.push(redactJsonLike(JSON.parse(line)) as HarnessEvent);
    } catch {
      malformedLineCount += 1;
    }
  }

  return {
    events,
    malformedLineCount,
    summary: summarizeReplayedEvents(events, malformedLineCount)
  };
}
