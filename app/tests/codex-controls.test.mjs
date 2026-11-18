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
const {CodexProcessControls,StopOutcome,stopLabel,StopRequests,appHome,ConversationStops,LastQuitNotice,lastQuitRecords,stopRequestsFor,labelOutcome}=load('CodexControls.tsx');
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

// After a quit with live work and a relaunch (DEL-01-02 REQ-005, AC-006): the
// turns the quit interrupted are said on the conversation, from the records only.
const DERIVED='The App session ended before a final status was recorded for this turn; this label is derived from that and is not written in any record.';
const quitRows=()=>[
  sr({stopRequestId:'stop:q1',appSession:'old',earlierSession:true,sourceSessionEnd:'established',cause:'quit',turnId:'tq1',requestedAt:'2026-10-11T09:00:00Z',state:'settled',label:'interrupted by quit',codexReported:'interrupted'}),
  sr({stopRequestId:'stop:q2',appSession:'old',earlierSession:true,sourceSessionEnd:'established',cause:'quit',turnId:'tq2',requestedAt:'2026-10-11T09:00:00Z',state:'accepted',label:'interrupted by quit (final status not observed)',labelDerived:true,reading:DERIVED,codexReported:null}),
  sr({stopRequestId:'stop:q3',appSession:'old',earlierSession:true,sourceSessionEnd:'established',cause:'quit',turnId:'tq3',requestedAt:'2026-10-11T09:00:00Z',state:'send-unknown',label:null,reading:"Stop requested; the interrupt's write began and its completion was not observed, so whether it reached Codex is not known.",codexReported:null}),
  sr({stopRequestId:'stop:q4',appSession:'old',earlierSession:true,sourceSessionEnd:'established',cause:'quit',threadId:'second',turnId:'tq4',requestedAt:'2026-10-11T09:00:00Z',state:'outcome-unknown',label:'interrupted by quit (final status not observed)',reading:'No final turn status is recorded for this stop request. That does not establish that Codex\'s process ended.',codexReported:null}),
  sr({stopRequestId:'stop:q5',appSession:'old',earlierSession:true,sourceSessionEnd:'established',cause:'quit',threadId:'keyed',home:'H-key',turnId:'tq5',requestedAt:'2026-10-11T09:00:00Z',state:'settled',label:'interrupted by quit',codexReported:'interrupted'}),
  // An older quit, and a request of a session whose end is not established: neither is "the last quit".
  sr({stopRequestId:'stop:q0',appSession:'older',earlierSession:true,sourceSessionEnd:'established',cause:'quit',threadId:'ancient',turnId:'tq0',requestedAt:'2026-10-01T09:00:00Z',state:'settled',label:'interrupted by quit',codexReported:'interrupted'}),
  sr({stopRequestId:'stop:qx',appSession:'other',earlierSession:false,sourceSessionEnd:'not-established',cause:'quit',turnId:'tqx',requestedAt:'2026-10-12T09:00:00Z',state:'sent',label:null,
    reading:'Recorded by another App session whose end is not established. No final status is recorded for this turn, and no label is derived.',codexReported:null}),
];

test('a conversation says which of its turns the quit interrupted, from the records only, and offers Continue',()=>{
  const requests={records:quitRows(),limits:[]};
  const rows=stopRequestsFor(requests,'thread','H-acct');
  assert.deepEqual(rows.map(r=>r.stopRequestId),['stop:q1','stop:q2','stop:q3','stop:qx']);
  assert.deepEqual(stopRequestsFor(requests,'thread','H-key'),[],'the ledger is App-wide; another home\'s rows are not this conversation\'s');
  assert.deepEqual(stopRequestsFor(requests,null,'H-acct'),[]);
  let continued=0;
  const html=renderToStaticMarkup(React.createElement(ConversationStops,{records:rows,onContinue:()=>{continued++;},canContinue:true}));
  const plain=agentPlain(html);
  assert.ok(html.includes('<b>A turn of this conversation was interrupted when you quit the App.</b> Codex reported it interrupted.'),html);
  assert.ok(html.includes('<b>A turn of this conversation was under way when you quit the App.</b> The App asked Codex to interrupt it; no final status was recorded for it, so the App labels it “interrupted by quit (final status not observed)”.'));
  // Each turn keeps its own label and reading; a derived label stays marked derived with what that means.
  assert.ok(plain.includes('App label: <b>interrupted by quit</b>. ⟦Reading: Final status observed when the turn ended.⟧ Codex reported: interrupted.'));
  assert.ok(plain.includes(`App label: <b>interrupted by quit (final status not observed)</b> (derived; not written). ⟦Reading: ${DERIVED}⟧`));
  // A send-unknown request is never an interrupt that reached Codex; another session's request keeps its reading and gets no label.
  const others=html.slice(html.indexOf('Other stop requests recorded for this conversation'));
  assert.ok(others.length<html.length,'the unlabelled requests are listed apart');
  assert.ok(agentPlain(others).includes("Stop request: ⟦Reading: Stop requested; the interrupt&#x27;s write began and its completion was not observed, so whether it reached Codex is not known.⟧"));
  assert.ok(agentPlain(others).includes('Stop request: ⟦Reading: Recorded by another App session whose end is not established. No final status is recorded for this turn, and no label is derived.⟧'));
  assert.ok(!others.includes('App label'),'no unlabelled request gets a label');
  // Nothing suggests a run end, an answered request or recovered delegated work.
  assert.ok(html.includes('An interrupted turn is not a workflow run&#x27;s end. Requests Codex was waiting on you for when the App quit or Codex was stopped were not answered, and this App session cannot answer them. Nothing here says what became of agents the conversation delegated work to.'));
  assert.ok(!/held|blocked/i.test(html),'plain words');
  assert.ok(html.includes('Continue this conversation</button>')&&html.includes('The App does not send the interrupted turn&#x27;s message again; nothing is sent until you write and send a message.'));
  assert.ok(!html.includes('A turn with no record here'),'no limit, no limit line');
  const limited=renderToStaticMarkup(React.createElement(ConversationStops,{records:rows,limited:true}));
  assert.ok(limited.includes('A turn with no record here is not shown to have run to its end.')&&!limited.includes('Continue this conversation'),'no offer without an act');
  assert.equal(renderToStaticMarkup(React.createElement(ConversationStops,{records:[]})),'','no record, nothing said: absence establishes nothing');
  assert.equal(continued,0,'rendering continues nothing');
  // The person's own interrupt is shown by the same display, with no quit sentence.
  const own=renderToStaticMarkup(React.createElement(ConversationStops,{records:[sr()]}));
  assert.ok(own.includes('Stop requests recorded for this conversation')&&own.includes('<b>interrupted by the person</b>')&&!own.includes('quit the App')&&!own.includes('were not answered'));
});

test('the last quit is said without a press, by conversation, in the active home only',()=>{
  const requests={records:quitRows(),limits:[]};
  assert.deepEqual(lastQuitRecords(requests).map(r=>r.stopRequestId),['stop:q1','stop:q2','stop:q3','stop:q4','stop:q5'],'the newest earlier session only; a session whose end is not established is not counted');
  assert.deepEqual(lastQuitRecords(requests,'H-acct').map(r=>r.stopRequestId),['stop:q1','stop:q2','stop:q3','stop:q4']);
  assert.deepEqual(lastQuitRecords({records:[sr()]}),[],'no quit, no notice');
  const name=id=>React.createElement('code',null,id);
  let selected=[];
  const html=renderToStaticMarkup(React.createElement(LastQuitNotice,{requests,home:'H-acct',name,select:id=>selected.push(id),selected:'second',canSelect:true,received:id=>id!=='second'}));
  assert.ok(html.includes('<b>When you last quit the App with work under way (stop requests recorded 2026-10-11T09:00:00Z), the App asked Codex to interrupt 3 turns in 2 conversations of this Codex home.</b>'),html);
  assert.ok(html.includes('<code>thread</code> · <span>interrupted by quit</span><span>; interrupted by quit (final status not observed) (derived; not written)</span> <button>Select this conversation</button>'));
  assert.ok(html.includes('<code>second</code> · <span>interrupted by quit (final status not observed)</span><small> (selected)</small>'));
  assert.ok(html.includes('For 1 other turn under way then, the record does not establish that the interrupt ended it'));
  assert.ok(html.includes('1 more stop request from that quit is recorded in another Codex home'));
  assert.ok(!html.includes('ancient')&&!html.includes('tqx'));
  assert.ok(html.includes('Nothing is continued or sent until you choose Continue.'));
  assert.deepEqual(selected,[]);
  const unreceived=renderToStaticMarkup(React.createElement(LastQuitNotice,{requests,home:'H-acct',name,select:()=>{},selected:null,canSelect:true,received:()=>false}));
  assert.ok(unreceived.includes('Not among the received conversations; read another page of stored conversations to find it.')&&!unreceived.includes('Select this conversation'));
  const workspace=renderToStaticMarkup(React.createElement(LastQuitNotice,{requests:{...requests,limits:['x']},home:'H-acct',name,open:React.createElement('a',{href:'#workspace-history'},'Open History'),dismiss:()=>{}}));
  assert.ok(workspace.includes('Open History and select the conversation')&&workspace.includes('<a href="#workspace-history">Open History</a>')&&workspace.includes('Hide this notice'));
  assert.ok(workspace.includes('A turn with no record here is not shown to have run to its end.'),'a limit is said, so absence is not read as nothing interrupted');
  // Another home's quit only: said, without counting this home's turns as interrupted.
  const keyed=renderToStaticMarkup(React.createElement(LastQuitNotice,{requests,home:'H-omlx',name}));
  assert.ok(keyed.includes('the App recorded stop requests in another Codex home.')&&keyed.includes('5 more stop requests from that quit are recorded in another Codex home'));
  assert.equal(appHome('local-provider'),'H-omlx');
});

test('a label says how the turn ended in the App\'s own words',()=>{
  assert.equal(labelOutcome('interrupted by quit'),'interrupted');
  assert.equal(labelOutcome('interrupted by quit (final status not observed)'),'unknown');
  assert.equal(labelOutcome('outcome unknown (stop requested)'),'unknown');
  assert.equal(labelOutcome('completed (quit requested)'),'completed');
  assert.equal(labelOutcome('failed (Stop Codex requested)'),'failed');
  assert.equal(labelOutcome('something else'),null);
  assert.equal(labelOutcome(null),null);
});
