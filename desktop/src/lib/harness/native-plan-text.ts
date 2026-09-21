/** Display projection only: recorded source events and their hashes stay unchanged. */
export function nativePlanText(revision: { sourceEvent: { plan: unknown } }): string {
  const plan = revision.sourceEvent.plan;
  if (typeof plan === 'string') return plan;
  if (plan !== null && typeof plan === 'object' && !Array.isArray(plan) &&
      'type' in plan && plan.type === 'plan' && 'text' in plan && typeof plan.text === 'string') return plan.text;
  return JSON.stringify(plan, null, 2) ?? '';
}
