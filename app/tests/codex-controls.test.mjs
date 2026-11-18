import test from 'node:test';
import {agentPlain} from './support/agent-text.mjs';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import {localRequire} from './support/load-src.mjs';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const load=name=>{const url=new URL(`../src/${name}`,import.meta.url);const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});const exports={};new Function('require','exports',compiled.outputText)(localRequire(createRequire(url)),exports);return exports;};
const {CodexProcessControls,StopOutcome,stopLabel,StopRequests,appHome,ConversationStops,PreviousQuitNotice,previousQuitRecords,stopRequestsFor,storedStopLabel,homeOfGeneration,historyHome,reportedFinal,continueEligible}=load('CodexControls.tsx');
const {StopLabel}=load('NativeActivity.tsx');
const g={appSession:'s',home:'h',spawnCounter:1};
const outcome={action:'Stop Codex',state:'stopped',confirmedAt:'2026-10-10T00:00:00Z',modeHomeClass:'account',generation:g,
  turns:[{threadId:'thread',turnId:'t1',label:'interrupted by Stop Codex',codexReported:'interrupted',interruptRequest:{state:'acknowledged',reading:"Codex acknowledged the interrupt request. An acknowledgment is not the turn's end."}},
    {threadId:'thread',turnId:'t2',label:'interrupted by Stop Codex (final status not observed)',codexReported:null,interruptRequest:{state:'acknowledged',reading:"Codex acknowledged the interrupt request. An acknowledgment is not the turn's end."}}],
  outstandingRequests:{count:1,reading:'Not answered by the App; they end unanswered with the Codex process.'},
  runsInForce:{rows:[{run:'run-1',conversation:'thread',workflow:{name:'coordinated-knowledge-work'},state:'open'}],reading:'Stopping Codex ends no workflow run.'},
  historyNote:'A turn still live at the stop: Codex may write into its history that the user interrupted the turn on purpose. That note comes from this stop.',
  records:"Recorded in the App's recovery ledger: a codex_stop record when you confirm, then a stop-request record for each interrupt before it is sent, with its outcome. After a relaunch the App reads the turns' labels back from these records. A record the ledger has not accepted is shown as not yet written and kept in this App process; the stop still proceeds. The outcome panel itself is kept in this App process only.",start:null,conversations:null};
const stops=outcomes=>({outcomes,stopWaitLimitSeconds:10,records:outcome.records});
const render=(host,act=()=>{})=>renderToStaticMarkup(React.createElement(CodexProcessControls,{host,busy:false,act}));

test('Stop and Restart ask first and are offered only while Codex runs',()=>{
  const ready=render({state:'ready',generation:g,codexStops:stops([])});
  assert.ok(ready.includes('Stop Codex…')&&ready.includes('Restart Codex…')&&ready.includes('Start Codex'));
  assert.equal((ready.match(/disabled=""/g)??[]).length,0);
  assert.ok(ready.includes('Stop Codex and Restart Codex ask first'));
  assert.ok(ready.includes('with no time limit')&&ready.includes('<b>Keep Codex running</b> (the default) and Cancel change nothing'));
  assert.ok(ready.includes('waits up to 10 s')&&ready.includes('no workflow run ends')&&ready.includes('continues no conversation until you choose <b>Continue selected conversation</b>'));
  assert.ok(ready.includes('your operational choice, not a recorded act'));
  assert.ok(ready.includes('Recorded in the App&#x27;s recovery ledger: a codex_stop record when you confirm, then a stop-request record for each interrupt before it is sent'),'what is recorded, and where, is stated');
  assert.ok(ready.includes('The outcome panel itself is kept in this App process only.'));
  for(const state of ['stopped','absent','refused','stopping']){
    const html=render({state,generation:g,codexStops:stops([])});
    assert.equal((html.match(/disabled=""/g)??[]).length,2,`${state}: Stop and Restart unavailable, Start available`);
  }
});

// Stop and Restart wiring is exercised in conversation-panel.test.mjs (mounted).

test('the outcome shows labels from turn status and keeps the acknowledgment apart',()=>{
  const html=renderToStaticMarkup(React.createElement(StopOutcome,{outcome}));
  assert.ok(html.includes('turn t1: <b>interrupted by Stop Codex</b> · Codex reported: interrupted'));
  assert.ok(html.includes('turn t2: <b>interrupted by Stop Codex (final status not observed)</b> · Codex reported no end before the stop'));
  assert.ok(html.includes("An acknowledgment is not the turn&#x27;s end"));
  assert.ok(!/turn ended|run ended|Stopped\b/.test(html),'no acknowledgment presented as turn end; never "Stopped"');
  assert.ok(html.includes('1 waiting request(s): Not answered by the App'));
  assert.ok(html.includes('coordinated-knowledge-work (run run-1). Stopping Codex ends no workflow run.'));
  assert.ok(html.includes('That note comes from this stop.'));
  const restart=renderToStaticMarkup(React.createElement(StopOutcome,{outcome:{...outcome,action:'Restart Codex',start:{state:'started'},conversations:'No conversation was continued automatically. To continue one, read stored conversations, select it and choose Continue selected conversation.'}}));
  assert.ok(restart.includes('Codex started again in a new process. No conversation was continued automatically.'));
  const none=renderToStaticMarkup(React.createElement(StopOutcome,{outcome:{...outcome,turns:[],outstandingRequests:{count:0},runsInForce:{rows:[]},historyNote:null}}));
  assert.ok(none.includes('No live turn was observed, so no interrupt was sent.'));
});

test('the activity shows the App label beside Codex status, newest outcome first',()=>{
  const older={...outcome,turns:[{...outcome.turns[0],label:'completed (Stop Codex requested)',codexReported:'completed'}]};
  const s=stops([older,outcome]);
  assert.equal(stopLabel(s,'thread','t1').label,'interrupted by Stop Codex');
  assert.equal(stopLabel(s,'thread','other'),null);
  assert.equal(stopLabel(s,'other','t1'),null);
  assert.equal(stopLabel(undefined,'thread','t1'),null);
  const html=renderToStaticMarkup(React.createElement(StopLabel,{stop:stopLabel(s,'thread','t2')}));
  assert.ok(html.includes('App label: <b>interrupted by Stop Codex (final status not observed)</b> (Codex reported no end before the stop)'));
  assert.equal(renderToStaticMarkup(React.createElement(StopLabel,{stop:null})),'');
});

test('a refused stop is a refusal: no Stop label for its turns, here or in the activity',()=>{
  const refused={...outcome,state:'stop refused',stop:{state:'refused',reading:'stop already requested for this source generation'},
    turns:[{threadId:'thread',turnId:'t1',label:null,codexReported:null,interruptRequest:{state:'acknowledged',reading:"Codex acknowledged the interrupt request. An acknowledgment is not the turn's end."}}],historyNote:null};
  const html=renderToStaticMarkup(React.createElement(StopOutcome,{outcome:refused}));
  assert.ok(html.includes('Codex not stopped: stop already requested for this source generation'));
  assert.ok(html.includes('turn t1: no Stop Codex label (Codex was not stopped) · Codex reported no end'));
  assert.ok(!html.includes('<b>interrupted by Stop Codex'),'no label shown');
  // A later stop that did not name t1 leaves no label either; an older stopped outcome still does.
  assert.equal(stopLabel(stops([refused]),'thread','t1'),null);
  assert.equal(stopLabel(stops([outcome,refused]),'thread','t1').label,'interrupted by Stop Codex');
});

// REC SR rows as the host reports them (stop_records::outcomes).
const sr=(over={})=>({stopRequestId:'stop:1',appSession:'s',earlierSession:false,home:'H-acct',generation:'gen',threadId:'thread',turnId:'t1',cause:'person-interrupt',
  requestedAt:'2026-10-10T00:00:01Z',state:'outcome-observed',label:'interrupted by the person',reading:'Final status observed when the turn ended.',codexReported:'interrupted',persistence:'recorded in the App ledger',...over});

test('stop-request records label turns first and read back after a relaunch (REC SR)',()=>{
  const requests={records:[sr(),sr({stopRequestId:'stop:2',turnId:'t3',appSession:'old',earlierSession:true,state:'sent',label:'outcome unknown (stop requested)',labelDerived:true,
    reading:'The App session ended before a final status was recorded for this turn.',codexReported:null}),
    sr({stopRequestId:'stop:3',turnId:'t4',state:'refused',label:null,reading:'Codex refused the stop request: no active turn',codexReported:null,persistence:'not yet written to the App ledger; kept in this App process'})],
    limits:[],standing:'App-observed stop requests (REC SR).'};
  // A recorded request is preferred to this process's Stop Codex outcome for the same turn.
  assert.equal(stopLabel(stops([outcome]),'thread','t1',requests).label,'interrupted by the person');
  assert.equal(stopLabel(stops([outcome]),'thread','t2',requests).label,'interrupted by Stop Codex (final status not observed)','no record: the outcome still labels');
  const label=renderToStaticMarkup(React.createElement(StopLabel,{stop:stopLabel(undefined,'thread','t1',requests)}));
  assert.ok(agentPlain(label).includes('App label: <b>interrupted by the person</b>. ⟦Reading: Final status observed when the turn ended.⟧ Codex reported: interrupted.'));
  assert.ok(agentPlain(label).includes('Record: ⟦Record: recorded in the App ledger⟧.'));
  const earlier=renderToStaticMarkup(React.createElement(StopLabel,{stop:stopLabel(undefined,'thread','t3',requests)}));
  assert.ok(earlier.includes('<b>outcome unknown (stop requested)</b> (derived; not written).')&&earlier.includes('From an earlier App session.'),earlier);
  assert.ok(!label.includes('derived'),'a recorded label is not marked derived');
  const refused=renderToStaticMarkup(React.createElement(StopLabel,{stop:stopLabel(undefined,'thread','t4',requests)}));
  // The reading carries Codex's refusal, so it stands boxed.
  assert.ok(agentPlain(refused).includes('Stop request: ⟦Reading: Codex refused the stop request: no active turn⟧')&&!refused.includes('App label'),refused);
  assert.ok(agentPlain(refused).includes('Record: ⟦Record: not yet written to the App ledger; kept in this App process⟧.'),'a write not yet accepted is visible');
  const listed=renderToStaticMarkup(React.createElement(StopRequests,{requests}));
  assert.ok(listed.includes('Recorded stop requests (3)'));
  assert.ok(listed.includes('turn t1 · your interrupt at 2026-10-10T00:00:01Z: <b>interrupted by the person</b>. Final status observed'));
  assert.ok(listed.includes('turn t3 · your interrupt at 2026-10-10T00:00:01Z (earlier App session): <b>outcome unknown (stop requested)</b> (derived; not written).'));
  assert.equal(renderToStaticMarkup(React.createElement(StopRequests,{requests:{records:[],limits:[]}})),'');
  assert.ok(render({state:'ready',generation:g,codexStops:stops([]),stopRequests:requests}).includes('Recorded stop requests (3)'));
  const bad=renderToStaticMarkup(React.createElement(StopRequests,{requests:{records:[],limits:['a stop_request ledger entry is not a valid stop-request record and is not shown: x']}}));
  assert.ok(bad.includes('Limit: a stop_request ledger entry is not a valid'));
  // The outcome says whether the codex_stop record and each turn's stop-request record were written.
  const html=renderToStaticMarkup(React.createElement(StopOutcome,{outcome:{...outcome,codexStopRecord:{state:'recorded',reading:'Recorded in the App ledger before any interrupt was sent'},
    turns:[{...outcome.turns[0],stopRequest:sr({cause:'codex-stop'})},{...outcome.turns[1],stopRequest:null}]}}));
  assert.ok(html.includes('Stop Codex record: Recorded in the App ledger before any interrupt was sent.'));
  assert.ok(html.includes('stop-request record: recorded in the App ledger'));
  assert.ok(html.includes('stop-request record: not recorded'));
  // The ledger is App-wide: a row of the other home does not label this home's turn.
  assert.equal(stopLabel(undefined,'thread','t1',requests,appHome('account')).label,'interrupted by the person');
  assert.equal(stopLabel(undefined,'thread','t1',requests,appHome('api-key')),null);
  assert.equal(appHome('other'),undefined);
});
// The App's pause of sends during Stop Codex, and the interrupt and selection
// controls that stay available, are exercised in conversation-panel.test.mjs.

// After a quit with live work and a relaunch (DEL-01-02 REQ-005, AC-006): what
// each record establishes is said on the conversation, and no more.
const DERIVED='The App session ended before a final status was recorded for this turn; this label is derived from that and is not written in any record.';
const UNKNOWN='The App recorded a quit stop request for this turn. The final outcome is unknown to the App.';
const QUIT_REPORTED='The App recorded a quit stop request for this turn. Codex reported it interrupted.';
const old=(over)=>sr({appSession:'old',earlierSession:true,sourceSessionEnd:'established',cause:'quit',requestedAt:'2026-10-11T09:00:00Z',send:'sent',...over});
const quitRows=()=>[
  old({stopRequestId:'stop:q1',turnId:'tq1',state:'settled',label:'interrupted by quit',codexReported:'interrupted'}),
  // SR-08 after a refused interrupt: written, outcome unknown.
  old({stopRequestId:'stop:q2',turnId:'tq2',state:'outcome-unknown',label:'interrupted by quit (final status not observed)',reading:'No final turn status is recorded for this stop request. That does not establish that Codex\'s process ended.',codexReported:null}),
  old({stopRequestId:'stop:q3',turnId:'tq3',state:'send-unknown',send:'unknown(write-incomplete)',label:null,reading:"Stop requested; the interrupt's write began and its completion was not observed, so whether it reached Codex is not known.",codexReported:null}),
  old({stopRequestId:'stop:q4',threadId:'second',turnId:'tq4',state:'accepted',label:'interrupted by quit (final status not observed)',labelDerived:true,reading:DERIVED,codexReported:null}),
  old({stopRequestId:'stop:q5',threadId:'keyed',home:'H-key',turnId:'tq5',state:'settled',label:'interrupted by quit',codexReported:'interrupted'}),
  old({stopRequestId:'stop:q0',appSession:'older',threadId:'ancient',turnId:'tq0',requestedAt:'2026-10-01T09:00:00Z',state:'settled',label:'interrupted by quit',codexReported:'interrupted'}),
  old({stopRequestId:'stop:qx',appSession:'other',earlierSession:false,sourceSessionEnd:'not-established',turnId:'tqx',requestedAt:'2026-10-12T09:00:00Z',state:'sent',label:null,
    reading:'Recorded by another App session whose end is not established. No final status is recorded for this turn, and no label is derived.',codexReported:null}),
];
const quitEnded={previousSession:'old',previousSessionEnd:'quit-with-live-work',previousSessionQuitStops:['stop:q1','stop:q2','stop:q3','stop:q4','stop:q5']};
const name=id=>React.createElement('code',null,id);
const notice=props=>renderToStaticMarkup(React.createElement(PreviousQuitNotice,{name,received:()=>true,...props}));

test('a conversation lists its stop requests by what each record establishes, and offers Continue only on a qualifying row',()=>{
  const requests={records:quitRows(),limits:[]};
  const rows=stopRequestsFor(requests,'thread','H-acct');
  assert.deepEqual(rows.map(r=>r.stopRequestId),['stop:q1','stop:q2','stop:q3','stop:qx']);
  assert.deepEqual(stopRequestsFor(requests,'thread',undefined),[],'an unknown home is never a wildcard');
  assert.deepEqual(stopRequestsFor(requests,'thread','H-key'),[]);
  let continued=0;
  const html=renderToStaticMarkup(React.createElement(ConversationStops,{records:rows,onContinue:()=>{continued++;},canContinue:true}));
  const plain=agentPlain(html);
  assert.ok(html.includes('aria-label="Stop requests recorded for this conversation"'));
  // Per record, never a count of turns, and no order of events or cause.
  assert.ok(plain.includes(`${QUIT_REPORTED} App label: <b>interrupted by quit</b>.`),plain);
  assert.ok(!/after the App sent|gives the cause|turns? of this conversation/.test(html));
  assert.ok(plain.includes(`${UNKNOWN} App label: <b>interrupted by quit (final status not observed)</b>. ⟦Reading: No final turn status is recorded`));
  assert.ok(!/you quit/.test(html),'no attribution to the person');
  // The request time is a recorded value, boxed.
  assert.ok(plain.includes('(quitting the App, requested ⟦Requested: 2026-10-11T09:00:00Z⟧, earlier App session)'),plain);
  // A send-unknown request and another session's request keep their readings, without a label.
  assert.ok(plain.includes("Stop request, no outcome label. ⟦Reading: Stop requested; the interrupt&#x27;s write began"));
  assert.ok(plain.includes('Stop request, no outcome label. ⟦Reading: Recorded by another App session whose end is not established.'));
  assert.ok(html.includes('Read turns asks Codex for a page of stored turns. An interrupted turn is not a workflow run&#x27;s end. An interrupt request does not answer a Codex request. Nothing here says what became of agents the conversation delegated work to.'));
  assert.ok(!/were not answered|cannot answer them|shown beside it|own status for each turn|held|blocked/i.test(html));
  assert.ok(html.includes('Continue this conversation</button> <small>Continue asks Codex to reopen this conversation. It opens after a matching resume is confirmed. Continue sends no conversation message.</small>'));
  assert.equal(continued,0,'rendering continues nothing');
  // With the handler supplied, no qualifying row means no added offer.
  for(const only of [[rows[2]],[rows[3]],[sr({send:'sent'})],[old({label:null,state:'not-sent',send:'not-sent(not-ready)',reading:'Stop not sent: x'})]]){
    const none=renderToStaticMarkup(React.createElement(ConversationStops,{records:only,onContinue:()=>{continued++;},canContinue:true}));
    assert.ok(!none.includes('Continue this conversation'),none);
  }
  assert.equal(continueEligible(sr()),false,'a current-session row: its session has not ended');
  assert.equal(continueEligible(rows[0]),true);
  assert.equal(continueEligible({label:'interrupted by Stop Codex',codexReported:'interrupted'}),false,'a memory-only outcome is not a qualifying record');
  const limited=renderToStaticMarkup(React.createElement(ConversationStops,{records:rows,limited:true}));
  assert.ok(limited.includes('The App&#x27;s reading of stop records has limits. See Recorded stop requests under Codex process. A turn with no record here is not shown to have run to its end.'));
  assert.ok(!limited.includes('Some stop records carry limits'));
  assert.equal(renderToStaticMarkup(React.createElement(ConversationStops,{records:[]})),'','no record, nothing said: absence establishes nothing');
  // An earlier interrupt row with its unknown label.
  const own=agentPlain(renderToStaticMarkup(React.createElement(ConversationStops,{records:[old({cause:'person-interrupt',label:'outcome unknown (stop requested)',codexReported:null})]})));
  assert.ok(own.includes('The App recorded an interrupt request for this turn. The final outcome is unknown to the App. App label: <b>outcome unknown (stop requested)</b>.'),own);
});

test('an unqualified label with no or another reported status is not called an interruption Codex reported',()=>{
  for(const [reported,words] of [[null,UNKNOWN],['completed','Codex reported the turn completed.']]){
    const html=agentPlain(renderToStaticMarkup(React.createElement(ConversationStops,{records:[old({label:'interrupted by quit',codexReported:reported})]})));
    assert.ok(html.includes(`${words} App label: <b>interrupted by quit</b>.`),html);
    assert.ok(!html.includes('Codex reported it interrupted'));
  }
});

test('the previous session\'s quit is said only where its recorded end is that quit, for the requests it names',()=>{
  const requests={records:quitRows(),limits:[],...quitEnded};
  assert.deepEqual(previousQuitRecords(requests).map(r=>r.stopRequestId),['stop:q1','stop:q2','stop:q3','stop:q4','stop:q5']);
  assert.deepEqual(previousQuitRecords({...requests,previousSession:undefined}),[],'no previous session named, nothing said');
  assert.deepEqual(previousQuitRecords({...requests,previousSession:'between'}),[],'an older quit is not said again');
  const html=notice({requests,home:'H-acct',inHistory:true,received:id=>id==='thread'});
  const plain=agentPlain(html);
  assert.ok(html.includes('aria-label="Stop requests of the App&#x27;s last quit"'));
  assert.ok(html.includes('<b>The App quit. Its end record names stop requests for turns the App had observed live.</b> For that quit, 3 interrupt requests were written to Codex in this Codex home.'),html);
  assert.ok(!/you quit|with work under way|recorded 2026|Latest request time/.test(html),'no attribution, no state at exit, no timestamp');
  assert.ok(plain.includes(`Turn <code>tq1</code>: ${QUIT_REPORTED} App label: <b>interrupted by quit</b>.`));
  assert.ok(plain.includes(`Turn <code>tq2</code>: ${UNKNOWN} App label: <b>interrupted by quit (final status not observed)</b>.`));
  assert.ok(plain.includes(`Turn <code>tq4</code>: ${UNKNOWN} App label: <b>interrupted by quit (final status not observed)</b> (derived; not written).`));
  // No Select control: History's own chooser makes the selection.
  assert.ok(!html.includes('<button'),'no control in the History copy');
  // A conversation not in the received list is said to be missing, in the History copy.
  assert.ok(html.indexOf('<code>second</code>')<html.indexOf('This conversation is missing from the received list.'));
  assert.equal(html.split('This conversation is missing from the received list.').length-1,1,'only the conversation not received');
  assert.ok(html.includes('For 1 other stop request in this Codex home, the App has no confirmed write to Codex.'));
  assert.ok(html.includes('1 stop request is recorded outside this Codex home.')&&!html.includes('Connection'),'counted; no direction to another home');
  assert.ok(!html.includes('ancient')&&!html.includes('tqx'));
  assert.ok(html.includes('Select an available conversation to inspect its stop requests. Continue is a separate choice.'));
  assert.ok(html.includes('This notice resumes no conversation and sends no conversation message.')&&!html.includes('until you choose Continue'));
  // No conversation received: no direction to select one.
  const none=notice({requests,home:'H-acct',inHistory:true,received:()=>false});
  assert.equal(none.split('This conversation is missing from the received list.').length-1,2);
  assert.ok(!none.includes('Select an available conversation'));
  // The workspace copy: the same received check, a link, Hide.
  const workspace=notice({requests:{...requests,limits:['x']},home:'H-acct',received:()=>false,open:React.createElement('a',{href:'#workspace-history'},'Open History.'),hide:()=>{}});
  assert.equal(workspace.split('This conversation is missing from the received list.').length-1,2,'the workspace copy says it too');
  assert.ok(workspace.includes('<a href="#workspace-history">Open History.</a>')&&!workspace.includes('Select an available conversation'));
  assert.ok(workspace.includes('Hide this notice</button> <small>Hidden in this window until it reloads. The History notice is still available.</small>'));
  assert.ok(workspace.includes('The App&#x27;s reading of stop records has limits. See Recorded stop requests under Codex process.'));
  // Another home only: counted, nothing listed, no direction.
  const keyed=notice({requests,home:'H-omlx',inHistory:true});
  assert.ok(keyed.includes('5 stop requests are recorded outside this Codex home.')&&!keyed.includes('Select an available')&&!keyed.includes('<li'),keyed);
  // The home in view not known: nothing listed, nothing counted.
  const unknown=notice({requests,home:undefined});
  assert.ok(unknown.includes('Which Codex home is in view is not established, so no conversation is listed.')&&!unknown.includes('<li')&&!unknown.includes('written to Codex')&&!unknown.includes('outside this Codex home'));
});

test('a failed quit followed by a system termination or an unrecorded end, and a list that omits rows, are not called that quit',()=>{
  const records=quitRows();
  for(const [end,words] of [['system-terminated','That session&#x27;s end is recorded as ended by the system.'],['ended-without-record','That session&#x27;s end was not recorded.']]){
    const html=notice({requests:{records,limits:[],previousSession:'old',previousSessionEnd:end,previousSessionQuitStops:null},home:'H-acct'});
    assert.ok(html.includes('aria-label="Stop requests from the previous App session"'));
    assert.ok(html.includes(`<b>The previous App session recorded quit stop requests.</b> ${words} In this Codex home, 3 interrupt requests were written to Codex.`),html);
    assert.ok(!/App quit\.|that quit|you quit/.test(html));
    assert.ok(agentPlain(html).includes(`Turn <code>tq1</code>: ${QUIT_REPORTED}`),'the per-turn facts stay');
  }
  // The end record names one request: the others are only absent from its list.
  const html=notice({requests:{records,limits:[],previousSession:'old',previousSessionEnd:'quit-with-live-work',previousSessionQuitStops:['stop:q4']},home:'H-acct'});
  assert.ok(html.includes('For that quit, 1 interrupt request was written to Codex in this Codex home.'),html);
  assert.ok(html.includes('<code>tq4</code>')&&!html.includes('<code>tq1</code>')&&!html.includes('<code>tq2</code>'));
  assert.ok(html.includes('3 quit stop requests in this Codex home are absent from the recorded quit&#x27;s list.'));
  assert.ok(!/another quit attempt|not from the quit that ended it/.test(html),'omission is not read as another attempt');
  // A held quit list that names none of these.
  const none=notice({requests:{records,limits:[],previousSession:'old',previousSessionEnd:'quit-with-live-work',previousSessionQuitStops:[]},home:'H-acct'});
  assert.ok(none.includes('The previous App session recorded quit stop requests.</b> That session&#x27;s recorded quit names none of these requests.'),none);
  // The start says quit, and no list is held.
  const unheld=notice({requests:{records,limits:[],previousSession:'old',previousSessionEnd:'quit-with-live-work',previousSessionQuitStops:null},home:'H-acct'});
  assert.ok(unheld.includes('The previous App session recorded quit stop requests.</b> The App recorded the session&#x27;s end as a quit. The held records do not supply its request list.'),unheld);
  assert.ok(!unheld.includes('names none'));
  // Only a request never written: no conversation, no interruption words.
  const unsent=notice({requests:{records:[records[2]],limits:[],previousSession:'old',previousSessionEnd:'ended-without-record',previousSessionQuitStops:null},home:'H-acct',inHistory:true});
  assert.ok(unsent.includes('no interrupt request is recorded as written to Codex')&&unsent.includes('For 1 other stop request in this Codex home, the App has no confirmed write to Codex.'));
  assert.ok(!unsent.includes('<li')&&!unsent.includes('Select an available')&&!/interrupted|shows what each record says/.test(unsent),unsent);
});

test('a stored turn is matched in its own home on both paths; a History source binds a home only where its home and generation agree',()=>{
  const accountOutcome={state:'stopped',modeHomeClass:'account',generation:{appSession:'s',home:'acct-home',spawnCounter:1},turns:[{threadId:'T',turnId:'U',label:'interrupted by Stop Codex',codexReported:'interrupted'}]};
  const stops={outcomes:[accountOutcome]};
  assert.equal(storedStopLabel(stops,'T','U',{records:[]},'H-key'),null,'another home\'s Stop Codex outcome is not this home\'s');
  assert.equal(storedStopLabel(stops,'T','U',{records:[]},'H-acct').label,'interrupted by Stop Codex');
  assert.equal(storedStopLabel(stops,'T','U',{records:[]},undefined),null);
  const ledger={records:[old({threadId:'T',turnId:'U',home:'H-acct'})]};
  assert.equal(storedStopLabel(undefined,'T','U',ledger,'H-key'),null,'another home\'s record is not this home\'s');
  assert.equal(storedStopLabel(undefined,'T','U',ledger,'H-acct').stopRequestId,'stop:1');
  const g1={appSession:'s',home:'acct-home',spawnCounter:1},g2={appSession:'s',home:'key-home',spawnCounter:1},g3={appSession:'s',home:'local-home',spawnCounter:1};
  const host={homeRouting:{activeModeHomeClass:'account',entries:[{modeHomeClass:'account',generation:g1},{modeHomeClass:'api-key',generation:g2},{modeHomeClass:'local-provider',generation:g3}]}};
  assert.equal(homeOfGeneration(host,g2),'H-key','the page\'s generation, not the router\'s active choice');
  assert.equal(homeOfGeneration(host,g3),'H-omlx','the stored views know the local home');
  assert.equal(homeOfGeneration(host,{...g2,spawnCounter:2}),undefined);
  assert.equal(homeOfGeneration({homeRouting:{entries:[{modeHomeClass:'account',generation:g1},{modeHomeClass:'api-key',generation:g1}]}},g1),undefined,'ambiguous: unknown');
  // A mixed History source: its home is B while its generation is home A's.
  assert.equal(historyHome(host,{home:'acct-home',generation:g1}),'H-acct');
  assert.equal(historyHome(host,{home:'key-home',generation:g1}),undefined,'home and generation disagree: nothing is bound');
  assert.equal(historyHome(host,{generation:g1}),undefined);
  assert.equal(reportedFinal('completed'),'completed');assert.equal(reportedFinal('inProgress'),null);assert.equal(reportedFinal(null),null);
});

test('the live caller keeps main\'s home mapping: a local route passes no home to the live matcher',()=>{
  // App.tsx passes appHome(activeModeHomeClass) to stopLabel; that mapping is main's.
  assert.equal(appHome('account'),'H-acct');assert.equal(appHome('api-key'),'H-key');
  assert.equal(appHome('local-provider'),undefined,'as on main');
  const ledger={records:[sr({threadId:'T',turnId:'U',home:'H-acct'})]};
  assert.equal(stopLabel(undefined,'T','U',ledger,appHome('local-provider')).stopRequestId,'stop:1','with no home the live matcher filters no home, as on main');
  const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
  assert.ok(app.includes('stopLabelFor={(thread, turn) => stopLabel(host?.codexStops, thread, turn, host?.stopRequests, appHome(host?.homeRouting?.activeModeHomeClass))}'),'the live caller is main\'s');
});
