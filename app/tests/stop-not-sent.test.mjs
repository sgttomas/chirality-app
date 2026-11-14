import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import {localRequire} from './support/load-src.mjs';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {agentPlain} from './support/agent-text.mjs';
// DEL-01-02: an interrupt that was not written (not sent within the stop
// limit, or its write's outcome unknown), and an earlier build's write-failure
// row, carry no Stop label. Each is shown by its reading, never as Codex not
// stopped, never as interrupted and never as sent. Readings are the host's
// words (codex_stop.rs, stop_records.rs, hosting.rs).
const load=name=>{const url=new URL(`../src/${name}`,import.meta.url);const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});const exports={};new Function('require','exports',compiled.outputText)(localRequire(createRequire(url)),exports);return exports;};
const {StopOutcome,StopRequests,stopLabel}=load('CodexControls.tsx');
const {StopLabel}=load('NativeActivity.tsx');
const shown=element=>renderToStaticMarkup(element).replaceAll('&#x27;',"'");
// The turn's own line of the outcome panel (the panel's heading names the action in bold).
const turnLine=html=>html.slice(html.indexOf('<li>'),html.indexOf('</li>')+5);

const NOT_WRITTEN='the interrupt could not be written within the stop limit';
const NOT_SENT=`Stop not sent: ${NOT_WRITTEN}`;
const SEND_UNKNOWN="Stop requested; the interrupt's write began and its completion was not observed, so whether it reached Codex is not known.";
const WRITE_UNFINISHED="write outcome unknown: the interrupt's write to Codex began and its completion was not observed within the stop limit, so whether it reached Codex is not known";
const EARLIER_WRITE_FAILURE='An earlier App build recorded an interrupt write failure; whether the interrupt reached Codex is not established.';
const explained=send=>`Codex's process was confirmed ended during Stop. No final status for this turn was observed. ${send}`;

const g={appSession:'s',home:'h',spawnCounter:1};
const row=over=>({stopRequestId:'stop:1',appSession:'s',earlierSession:false,home:'H-acct',generation:'gen',threadId:'thread',turnId:'t1',cause:'codex-stop',
  requestedAt:'2026-11-13T00:00:00Z',label:null,labelDerived:false,codexReported:null,persistence:'recorded in the App ledger',sourceSessionEnd:'current',...over});
const rows={
  'send-unknown':row({state:'send-unknown',send:'unknown(write-incomplete)',response:'unknown-no-response',transition:'SR-13',reading:SEND_UNKNOWN}),
  'not sent within the stop limit':row({state:'not-sent',send:'not-sent(not-ready)',response:'not-applicable',transition:'SR-03',reading:NOT_SENT}),
  'an earlier build\'s write failure (0.2)':row({cause:'person-interrupt',earlierSession:true,sourceSessionEnd:'established',state:'not-sent',send:'not-sent(write-failed)',response:'not-applicable',transition:'SR-03',reading:EARLIER_WRITE_FAILURE}),
};
const turns={
  'send-unknown':{threadId:'thread',turnId:'t1',label:null,codexReported:null,reading:explained(SEND_UNKNOWN),interruptRequest:{state:'write outcome unknown',reading:WRITE_UNFINISHED},stopRequest:rows['send-unknown']},
  'not sent within the stop limit':{threadId:'thread',turnId:'t1',label:null,codexReported:null,reading:explained(NOT_SENT),interruptRequest:{state:'not sent',reading:NOT_WRITTEN},stopRequest:rows['not sent within the stop limit']},
};
const outcome=turn=>({action:'Stop Codex',state:'stopped',confirmedAt:'2026-11-13T00:00:00Z',modeHomeClass:'account',generation:g,turns:[turn],
  outstandingRequests:{count:0},runsInForce:{rows:[]},historyNote:null,records:'',start:null,conversations:null});

/** No label, no "not stopped", no "interrupted", and no claim that it was sent. */
function claimsNothing(html,name,{notSent}){
  assert.ok(!html.includes('<b>'),`${name}: no label: ${html}`);
  assert.ok(!/not stopped/i.test(html),`${name}: Codex was stopped: ${html}`);
  assert.ok(!/interrupted/i.test(html),`${name}: never interrupted: ${html}`);
  assert.ok(!/was sent|interrupt sent|sent to Codex|acknowledged/i.test(html),`${name}: never sent: ${html}`);
  if(!notSent) assert.ok(!/not sent/i.test(html),`${name}: neither sent nor not sent: ${html}`);
}

test('a stopped turn whose interrupt was not written shows its reading, not "Codex was not stopped"',()=>{
  for(const [name,turn] of Object.entries(turns)){
    const html=shown(React.createElement(StopOutcome,{outcome:outcome(turn)}));
    assert.ok(html.includes('Codex stopped'),name);
    assert.ok(html.includes(`turn t1: ${turn.reading} · Codex reported no end before the stop`),`${name}: ${html}`);
    claimsNothing(turnLine(html),name,{notSent:turn.interruptRequest.state==='not sent'});
  }
  // With no turn reading, the stop-request record's reading is shown.
  const html=shown(React.createElement(StopOutcome,{outcome:outcome({...turns['send-unknown'],reading:undefined})}));
  assert.ok(html.includes(`turn t1: ${SEND_UNKNOWN}`),html);
  claimsNothing(turnLine(html),'send-unknown, record reading',{notSent:false});
});

test('each row is shown by its reading in the recorded stop requests and the activity',()=>{
  for(const [name,record] of Object.entries(rows)){
    const notSent=record.reading===NOT_SENT;
    const list=shown(React.createElement(StopRequests,{requests:{records:[record],limits:[]}}));
    assert.ok(list.includes(record.reading),`${name}: ${list}`);
    claimsNothing(list,name,{notSent});
    const found=stopLabel({outcomes:[]},'thread','t1',{records:[record]},'H-acct');
    assert.equal(found,record,name);
    const note=shown(React.createElement(StopLabel,{stop:found}));
    // The reading can carry Codex's refusal, so it stands boxed beside the App's words.
    assert.ok(agentPlain(note).includes(`Stop request: ⟦Reading: ${record.reading}⟧`),`${name}: ${note}`);
    assert.ok(!note.includes('App label'),`${name}: ${note}`);
    claimsNothing(note,name,{notSent});
  }
});
