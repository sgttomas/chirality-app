import type { HarnessEvent } from '@chirality/runtime-contracts/event-schema';

export type SteeringReceipt = {
  sessionId: string; operationId: string; expectedTurnId: string; text: string;
  status: 'submitted' | 'accepted' | 'rejected' | 'unknown'; message?: string;
};
const storageKey = (sessionId: string) => `chirality:steering-receipts:${sessionId}`;
export function mergeSteeringReceipt(receipts: readonly SteeringReceipt[], incoming: SteeringReceipt): SteeringReceipt[] {
  const index = receipts.findIndex(row => row.sessionId === incoming.sessionId && row.operationId === incoming.operationId);
  if (index < 0) return [...receipts, incoming];
  const prior = receipts[index];
  if (prior.expectedTurnId !== incoming.expectedTurnId || prior.text !== incoming.text || (prior.status === 'accepted' && incoming.status !== 'accepted')) return [...receipts];
  return receipts.map((row, i) => i === index ? incoming : row);
}
function valid(value: unknown, sessionId: string): value is SteeringReceipt {
  const row = value as Partial<SteeringReceipt> | null;
  return Boolean(row && row.sessionId === sessionId && typeof row.operationId === 'string' && row.operationId && typeof row.expectedTurnId === 'string' && row.expectedTurnId && typeof row.text === 'string');
}
/** Local records retain delivery identity, never establish receipt after reload. */
export function recoverSteeringReceipts(sessionId: string, events: readonly HarnessEvent[], storage?: Pick<Storage, 'getItem'>): SteeringReceipt[] {
  let receipts: SteeringReceipt[] = [];
  try {
    const saved: unknown = JSON.parse(storage?.getItem(storageKey(sessionId)) ?? '[]');
    if (Array.isArray(saved)) receipts = saved.filter(row => valid(row, sessionId)).map(row => ({ ...row, status: 'unknown' as const, message: 'Check delivery to confirm this locally retained update.' }));
  } catch { /* Canonical events can still recover delivery identity. */ }
  for (const event of events) {
    if (event.sessionId !== sessionId || event.type !== 'codex.steer') continue;
    const data = event.data ?? {};
    const row = { ...data, sessionId, expectedTurnId: data.expectedTurnId ?? event.turnId };
    if (!valid(row, sessionId)) continue;
    receipts = mergeSteeringReceipt(receipts, { ...row, status: data.status === 'accepted' ? 'accepted' : data.status === 'rejected' ? 'rejected' : 'unknown' });
  }
  return receipts;
}
export function persistSteeringReceipt(receipt: SteeringReceipt, storage?: Pick<Storage, 'getItem' | 'setItem'>): void {
  if (!storage) return;
  try {
    const saved: unknown = JSON.parse(storage.getItem(storageKey(receipt.sessionId)) ?? '[]');
    const records = Array.isArray(saved) ? saved.filter(row => valid(row, receipt.sessionId)) : [];
    storage.setItem(storageKey(receipt.sessionId), JSON.stringify(mergeSteeringReceipt(records, receipt)));
  } catch { /* The in-memory receipt and canonical event journal remain available. */ }
}
