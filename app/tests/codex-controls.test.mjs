import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const load=name=>{const url=new URL(`../src/${name}`,import.meta.url);const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});const exports={};new Function('require','exports',compiled.outputText)(createRequire(url),exports);return exports;};
const {CodexProcessControls,StopOutcome,stopLabel,StopRequests}=load('CodexControls.tsx');
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

test('the controls call only the asking command',()=>{
  const source=readFileSync(new URL('../src/CodexControls.tsx',import.meta.url),'utf8')+readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
  assert.ok(!source.includes('host_stop'),'no unconfirmed stop command remains in the UI');
  assert.ok(source.includes('act("codex_stop", { generation: host?.generation, restart: false })')&&source.includes('act("codex_stop", { generation: host?.generation, restart: true })'));
});

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
  const requests={records:[sr(),sr({stopRequestId:'stop:2',turnId:'t3',appSession:'old',earlierSession:true,state:'sent',label:'outcome unknown (stop requested)',
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
  assert.ok(earlier.includes('<b>outcome unknown (stop requested)</b>')&&earlier.includes('From an earlier App session.'),earlier);
  const refused=renderToStaticMarkup(React.createElement(StopLabel,{stop:stopLabel(undefined,'thread','t4',requests)}));
  assert.ok(refused.includes('Stop request: Codex refused the stop request: no active turn')&&!refused.includes('App label'),refused);
  assert.ok(refused.includes('Record: not yet written to the App ledger; kept in this App process.'),'a write not yet accepted is visible');
  const listed=renderToStaticMarkup(React.createElement(StopRequests,{requests}));
  assert.ok(listed.includes('Recorded stop requests (3)'));
  assert.ok(listed.includes('turn t1 · your interrupt at 2026-10-10T00:00:01Z: <b>interrupted by the person</b>. Final status observed'));
  assert.ok(listed.includes('turn t3 · your interrupt at 2026-10-10T00:00:01Z (earlier App session)'));
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
  const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
  assert.ok(app.includes('stopLabel(host?.codexStops, thread, turn, host?.stopRequests)'));
});

test('conversation sends are paused while Stop or Restart Codex runs',()=>{
  const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
  assert.ok(app.includes('<ConversationPanel codexBusy={processBusy}'));
  assert.ok(app.includes('const busy = ownBusy || (codexBusy ? "Stop or Restart Codex in progress" : "");'));
  // Interrupting stays available during a stop; only the panel's own operation blocks it.
  assert.ok(app.includes('!live || !!ownBusy || alreadyRequested} onClick={interruptTurn}'));
  assert.ok(app.includes('<select disabled={!!ownBusy} value={threadKey}')&&app.includes('<select disabled={!!ownBusy} value={turnId}'));
});
