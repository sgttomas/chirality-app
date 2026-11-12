import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const load=name=>{const url=new URL(`../src/${name}`,import.meta.url);const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});const exports={};new Function('require','exports',compiled.outputText)(createRequire(url),exports);return exports;};
const {CodexProcessControls,StopOutcome,stopLabel,StopRequests,appHome}=load('CodexControls.tsx');
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
// A status names its active home; a host given here without one is given the account home.
const render=(host,act=()=>{})=>renderToStaticMarkup(React.createElement(CodexProcessControls,{host:host&&{homeRouting:{activeModeHomeClass:'account'},...host},busy:false,act}));

test('Stop and Restart ask first and are offered only while Codex runs',()=>{
  const ready=render({state:'ready',generation:g,codexStops:stops([])});
  assert.ok(ready.includes('Stop Codex…')&&ready.includes('Restart Codex…')&&ready.includes('Start Codex'));
  // The host accepts a start only from absent, stopped or refused (hosting.rs Host::start), so Start is not offered while Codex runs.
  assert.equal((ready.match(/disabled=""/g)??[]).length,1);assert.match(ready,/<button disabled="">Start Codex<\/button>/);
  assert.ok(ready.includes('Stop Codex and Restart Codex ask first'));
  assert.ok(ready.includes('with no time limit')&&ready.includes('<b>Keep Codex running</b> (the default) and Cancel change nothing'));
  assert.ok(ready.includes('waits up to 10 s')&&ready.includes('no workflow run ends')&&ready.includes('continues no conversation until you choose <b>Continue selected conversation</b>'));
  assert.ok(ready.includes('your operational choice, not a recorded act'));
  assert.ok(ready.includes('Recorded in the App&#x27;s recovery ledger: a codex_stop record when you confirm, then a stop-request record for each interrupt before it is sent'),'what is recorded, and where, is stated');
  assert.ok(ready.includes('The outcome panel itself is kept in this App process only.'));
  for(const state of ['stopped','absent','refused']){
    const html=render({state,generation:g,codexStops:stops([])});
    assert.equal((html.match(/disabled=""/g)??[]).length,2,`${state}: Stop and Restart unavailable, Start available`);
    assert.match(html,/<button>Start Codex<\/button>/);
  }
  assert.equal((render({state:'stopping',generation:g,codexStops:stops([])}).match(/disabled=""/g)??[]).length,3,'nothing is offered while a stop is under way');
});

test('after Codex ends unexpectedly the controls say which one starts it again',()=>{
  const html=render({state:'exited-unexpectedly',generation:g,generationClosed:true,codexStops:stops([])});
  assert.match(html,/<button disabled="">Start Codex<\/button>/,'the host refuses a start from this state, so it is not offered');
  assert.match(html,/<button>Stop Codex…<\/button>/);assert.match(html,/<button>Restart Codex…<\/button>/);
  assert.match(html,/<p role="status">Codex ended unexpectedly, so Start Codex is not available yet\. Choose <b>Restart Codex…<\/b> to start it again, or <b>Stop Codex…<\/b> to settle the ended process first; nothing is sent to it either way\.<\/p>/);
  assert.doesNotMatch(render({state:'ready',generation:g,codexStops:stops([])}),/ended unexpectedly/);
});

// Every host state against what the host accepts: Host::start only from absent, stopped or refused
// (hosting.rs start); a stop (and so Restart) from any other state but stopping, for the current full
// generation (hosting.rs stop_scoped, stop_inner). A sentence is shown only where its control is enabled.
test('each host state offers exactly the controls the host accepts from it',()=>{
  const STATES=[undefined,'absent','verifying','spawning','handshaking','ready','stopping','stopped','refused','exited-unexpectedly','halted-after-repeated-failure'];
  const exited=/Codex ended unexpectedly, so Start Codex is not available yet\. Choose <b>Restart Codex…<\/b> to start it again, or <b>Stop Codex…<\/b> to settle the ended process first; nothing is sent to it either way\./;
  const halted=/<p role="status">Codex failed to start, so Start Codex is not available\. Choose <b>Restart Codex…<\/b> to try again, or <b>Stop Codex…<\/b> to settle the failed start first\.<\/p>/;
  for(const state of STATES) for(const generation of [g,null]){
    const html=render({state,generation,codexStops:stops([])});
    const enabled=label=>new RegExp(`<button>${label}</button>`).test(html);
    const start=['absent','stopped','refused'].includes(state);
    const stop=!!generation&&!['absent','stopped','refused','stopping',undefined].includes(state);
    const at=`${state} ${generation?'with':'without'} a generation`;
    assert.equal(enabled('Start Codex'),start,`${at}: Start`);
    assert.equal(enabled('Stop Codex…'),stop,`${at}: Stop`);
    assert.equal(enabled('Restart Codex…'),stop,`${at}: Restart`);
    assert.equal(exited.test(html),state==='exited-unexpectedly'&&!!generation,`${at}: the unexpected-exit sentence`);
    assert.equal(halted.test(html),state==='halted-after-repeated-failure'&&!!generation,`${at}: the failed-start sentence`);
  }
});

// A start names its home and is accepted only from a known state: with the status not read, or
// the active home not reported, no control is offered at all.
test('Start Codex is not offered on an unread status or an unresolved home',()=>{
  const none=html=>assert.equal((html.match(/disabled=""/g)??[]).length,3,html.slice(0,200));
  none(render(null));none(render(undefined));none(render({codexStops:stops([])}));
  for(const state of ['absent','stopped','refused']){
    none(render({state,generation:null,homeRouting:undefined,codexStops:stops([])}));
    none(render({state,generation:null,homeRouting:{},codexStops:stops([])}));
    assert.match(render({state,generation:null,homeRouting:{activeModeHomeClass:'local-provider'},codexStops:stops([])}),/<button>Start Codex<\/button>/);
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
  assert.ok(label.includes('App label: <b>interrupted by the person</b>. Final status observed when the turn ended. Codex reported: interrupted.'));
  assert.ok(label.includes('Record: recorded in the App ledger.'));
  const earlier=renderToStaticMarkup(React.createElement(StopLabel,{stop:stopLabel(undefined,'thread','t3',requests)}));
  assert.ok(earlier.includes('<b>outcome unknown (stop requested)</b> (derived; not written).')&&earlier.includes('From an earlier App session.'),earlier);
  assert.ok(!label.includes('derived'),'a recorded label is not marked derived');
  const refused=renderToStaticMarkup(React.createElement(StopLabel,{stop:stopLabel(undefined,'thread','t4',requests)}));
  assert.ok(refused.includes('Stop request: Codex refused the stop request: no active turn')&&!refused.includes('App label'),refused);
  assert.ok(refused.includes('Record: not yet written to the App ledger; kept in this App process.'),'a write not yet accepted is visible');
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
  // The local-provider home has its own App-owned code: its lookup is filtered like the others, so
  // equal ids in another home never label its turn, and its own row does.
  assert.equal(appHome('local-provider'),'H-omlx');
  assert.equal(stopLabel(undefined,'thread','t1',requests,appHome('local-provider')),null,'the account home\u2019s row is not the local home\u2019s');
  const localRows={...requests,records:requests.records.map(r=>({...r,home:'H-omlx'}))};
  assert.equal(stopLabel(undefined,'thread','t1',localRows,appHome('local-provider')).label,'interrupted by the person');
  assert.equal(stopLabel(undefined,'thread','t1',localRows,appHome('account')),null);
  assert.equal(appHome('other'),undefined);
});
// The App's pause of sends during Stop Codex, and the interrupt and selection
// controls that stay available, are exercised in conversation-panel.test.mjs.
