import { NextResponse } from 'next/server';
import { asHarnessError, HarnessError } from '@chirality/runtime-contracts/errors';
import { HarnessErrorResponse } from '@chirality/runtime-contracts/types';

export async function readJsonBody<T>(request: Request): Promise<T> {
  try {
    return (await request.json()) as T;
  } catch {
    throw new HarnessError('INVALID_REQUEST', 400, 'Request body must be valid JSON');
  }
}

export function requireNonEmptyString(value: unknown, field: string): string {
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new HarnessError('INVALID_REQUEST', 400, `Missing or invalid '${field}'`);
  }

  return value.trim();
}

export function requireStringArray(value: unknown, field: string): string[] {
  if (!Array.isArray(value) || value.some((item) => typeof item !== 'string')) {
    throw new HarnessError('INVALID_REQUEST', 400, `Field '${field}' must be an array of strings`);
  }

  return value;
}

export function errorResponse(error: unknown): NextResponse<HarnessErrorResponse> {
  const harnessError = asHarnessError(error);
  return NextResponse.json(
    {
      error: {
        type: harnessError.type,
        message: harnessError.message,
        details: harnessError.details
      }
    },
    { status: harnessError.status }
  );
}

/**
 * One browser-facing SSE frame. `id` carries the Runtime turn registry's frame
 * sequence so a renderer can re-attach with `after=<seq>` after a dropped
 * connection (D-GOV-43 section 5).
 */
export function formatSseEvent(event: string, data: unknown, id?: number): string {
  const idLine = typeof id === 'number' && Number.isFinite(id) ? `id: ${Math.floor(id)}\n` : '';
  return `${idLine}event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
}

/** Comment-frame cadence on the browser-facing turn stream; matches the Runtime socket cadence. */
export const TURN_STREAM_KEEPALIVE_MS = 15_000;

/** Streams Runtime turn frames to the browser; closing the response only unsubscribes. */
export function turnStreamResponse(turn: {
  events: AsyncIterable<{ type: string; data: unknown; seq?: number }>;
  cancel(): Promise<void>;
}): Response {
  const encoder = new TextEncoder();
  // The Runtime's own comment keepalives are consumed by the runtime client,
  // so this proxy emits its own: a silent tool run must not look like a dead
  // stream to the renderer or to anything between them.
  let keepalive: ReturnType<typeof setInterval> | undefined;
  const stopKeepalive = (): void => {
    if (keepalive !== undefined) {
      clearInterval(keepalive);
      keepalive = undefined;
    }
  };
  const stream = new ReadableStream<Uint8Array>({
    async start(controller): Promise<void> {
      // The port returns only after Runtime has accepted the SSE subscription.
      // This is transport evidence; proxy keepalives below are not.
      controller.enqueue(encoder.encode(formatSseEvent('transport:connected', {})));
      keepalive = setInterval(() => {
        try {
          controller.enqueue(encoder.encode(': keepalive\n\n'));
        } catch {
          stopKeepalive();
        }
      }, TURN_STREAM_KEEPALIVE_MS);
      try {
        for await (const frame of turn.events) {
          controller.enqueue(encoder.encode(formatSseEvent(frame.type, frame.data, frame.seq)));
        }
      } catch (error) {
        stopKeepalive();
        try {
          controller.error(error);
        } catch {
          // Stream may already be closed/cancelled.
        }
        return;
      }
      stopKeepalive();
      try {
        controller.close();
      } catch {
        // Stream may already be closed/cancelled.
      }
    },
    async cancel(): Promise<void> {
      // The browser went away (navigation, reload, window close). The Runtime
      // keeps owning the turn; only this observer is released.
      stopKeepalive();
      await turn.cancel();
    }
  });
  return new Response(stream, {
    status: 200,
    headers: {
      'Content-Type': 'text/event-stream; charset=utf-8',
      'Cache-Control': 'no-cache, no-transform',
      Connection: 'keep-alive'
    }
  });
}
