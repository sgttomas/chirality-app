import { NextResponse } from 'next/server';
import { errorResponse } from '../../../../lib/harness/http';
import { getDaemonHarnessPort } from '../../../../lib/runtime-client/daemon-harness-port';

/**
 * GET /api/harness/agents — enumerate the agent roster (name + parsed
 * type/class) for the persona picker. `?directChat=1` restricts the result to
 * Type-0/Type-1 personas (D-APP-24), so the picker can never surface a Type-2
 * task agent for ad-hoc direct chat.
 */
export async function GET(request: Request): Promise<Response> {
  try {
    const url = new URL(request.url);
    const directChatOnly = url.searchParams.get('directChat') === '1';

    const result = await getDaemonHarnessPort().listAgents(
      { directChatOnly },
      { signal: request.signal }
    );
    return NextResponse.json(result, { status: 200 });
  } catch (error) {
    return errorResponse(error);
  }
}
