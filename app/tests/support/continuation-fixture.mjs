// Invented, bounded context returned only after an explicitly admitted resume.
export function continuationFixture({generation, threadId = 'stored', resumeRequestRef = 'req:resume', state = 'partial', revision = 1, admissionSelectionEpoch = 1, items} = {}) {
  const query = (kind, query_id) => ({factory_id: 91, query_id, home: generation.home, generation: structuredClone(generation), method: `thread/${kind}/list`, params: {threadId, sortDirection: 'desc', limit: kind === 'turns' ? 20 : 50, ...(kind === 'turns' ? {itemsView: 'summary'} : {turnId: 'prior-turn'})}});
  const turns = query('turns', 1), itemQuery = query('items', 2);
  const pending = ['queued', 'reading'].includes(state);
  const entries = items ?? [
    {id: 'prior-user', type: 'userMessage', content: [{type: 'text', text: 'Prior person message'}]},
    {id: 'prior-plan', type: 'plan', text: 'Prior plan: inspect then repair'},
    {id: 'prior-tool', type: 'commandExecution', command: 'inspect sample', status: 'completed', exitCode: 0, aggregatedOutput: 'Prior tool output'},
    {id: 'prior-agent', type: 'agentMessage', text: 'Prior agent response'},
  ];
  const resolution = query => ({query, revision: 1, outcome: pending ? 'pending' : 'native-result-observed'});
  return {home: generation.home, generation: structuredClone(generation), threadId, resumeRequestRef, admissionSelectionEpoch, revision, sourceCurrent: true, state, error: null, selectedTurnId: 'prior-turn', pageLimits: {turns: 20, items: 50}, partial: true, fullHistoryRebuilt: false, durableNativeData: false,
    history: {home: generation.home, generation: structuredClone(generation), state: 'history-receiving', selectionEpoch: 1,
      selected: {threadId, state: 'indexed-read-only', turnsPage: {data: [{id: 'prior-turn', status: 'completed', itemsView: 'summary', items: [entries[0], entries.at(-1)]}], nextCursor: 'older-turns', backwardsCursor: 'newer-turns'}, itemsPage: {data: entries.map(item => ({turnId: 'prior-turn', item})), nextCursor: 'older-items', backwardsCursor: 'newer-items'},
        streamResolutions: {'turn-pages': resolution(turns), 'item-pages': resolution(itemQuery)}, errorsByStream: {}}},
    receipts: [turns, itemQuery].map((query, i) => ({query, generation: structuredClone(generation), home: generation.home, sourceCurrent: true, requestRef: `req:context:${i}`, requestIdentity: i + 10, writeResult: 'written', outcome: pending ? 'pending' : 'response-observed-result', receiptPosition: i + 4, observedAt: '2026-10-18T00:00:00Z'})),
  };
}
