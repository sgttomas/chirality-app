import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {localRequire} from './support/load-src.mjs';
const load=name=>{const url=new URL(`../src/${name}`,import.meta.url);const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});const exports={};new Function('require','exports',compiled.outputText)(localRequire(createRequire(url)),exports);return exports;};
const {ArrivalRecord,CheckpointGuidance,RunBringBackView,RunPanel,runBringBackDefault,DeclaredPart,SelectedWorkflow,CompatibilityAdvisory,outputStanding,StandingFacets,arrivalLabel,actLabel,RecordWriteNotice}=load('RunPanel.tsx');
const h=(c,p)=>renderToStaticMarkup(React.createElement(c,p));

// The host's reading of the maintained valid example (workflow_declaration::read's shape).
const raw=JSON.parse(readFileSync(new URL('../src-tauri/resources/workflow_role/workflow-declaration.valid.example.json',import.meta.url),'utf8'));
const cats=['expected_inputs','required_tools','checkpoints','returned_outputs','returned_evidence'];
const declaration=(doc=raw)=>({raw:doc,reading:'recognized',findings:[],
  categories:Object.fromEntries(cats.map(c=>[c,doc[c]===undefined?'undeclared':doc[c].length?'recognized':'declared_empty'])),
  elements:Object.fromEntries(cats.filter(c=>Array.isArray(doc[c])).map(c=>[c,doc[c].map(value=>({value,reading:'recognized',findings:[]}))]))});
const record=kinds=>kinds.map((kind,i)=>({kind,recordId:`r${i}`,observedAt:'t',written:true,limit:null}));
const run=(over={})=>({reference:'run-1',conversation:'thread',workflow:{origin:'project',name:'resolve-spacing',revision:'abcdef0123456789'},
  lifecycle:{state:'open (live); only the person\'s explicit end ends it',records:record(['run_opened','supplied_guidance'])},
  compatibility:[{occasionLabel:'CK-2 run start',statement:'requirement check not established; the person may still start',notCurrent:false,r14:'no report published; no R14 written',
    publication:{state:'not published'},preparation:{declaration:declaration(),role:{standing:'app-observed',role:'WORKING_ITEMS',supply_ref:'sup:1'},
      check:{result:'not_established',tools:[],findings:[]},requirements:[{name:'read-supports',purpose:'Read',fallback:null,outcome:'present_currently_unavailable',reason:'host reported unavailable'}]}}],...over});
// PD-6 / OV-3 / SD-4: words a run state never takes.
const FORBIDDEN=/\bblocked\b|\bpaused\b|waiting for the person|hold support|not enforceable|unsupported|\bon hold\b|\bheld\b(?! actions)|\bre-held\b/i;

test('the declared part is readable: inputs, tools, checkpoints, outputs and evidence',()=>{
  const html=h(DeclaredPart,{declaration:declaration()});
  for(const name of ['run','spacing-limit','supports-table','read-supports','host-spacing-check','CP-accept'])assert.ok(html.includes(`<b>${name}</b>`),name);
  assert.ok(html.includes('read from the host through read-supports'));
  assert.ok(html.includes('Fallback: Examination only'));
  assert.ok(html.includes('<b>CP-accept</b>: accept by you on the change items of a named proposal, when add-support, set-stiffness report queued.'));
  assert.ok(html.includes('Where the act is performed: in the host&#x27;s own view'));
  assert.ok(html.includes('If declined: return to Propose'));
  assert.ok(html.includes('plan guidance in this phase; nothing is stopped'));
  for(const out of raw.returned_outputs){assert.ok(html.includes(`<b>${out.name}</b>`));}
  assert.ok(html.includes('Declared promise, not a standing:'));
  assert.ok(html.includes('Declared part as the host read it (JSON)'),'the source stays inspectable');
  assert.ok(!FORBIDDEN.test(html),html.match(FORBIDDEN)?.[0]);
});

test('a checkpoint is guidance: never a hold or block, governed changes nothing, invalid is a finding',()=>{
  const doc=structuredClone(raw);doc.checkpoints[0].governed='yes';
  const d=declaration(doc);d.elements.checkpoints[1]={value:{...doc.checkpoints[1],required_act:'A3'},reading:'invalid',findings:['FB-03: recognized act not permitted as checkpoint']};
  const html=h(RunPanel,{run:run({compatibility:[{...run().compatibility[0],preparation:{...run().compatibility[0].preparation,declaration:d}}]})});
  assert.ok(html.includes('Declared governed. In this phase that changes nothing'));
  assert.ok(html.includes('<b>Declaration finding: invalid</b> (FB-03'));
  assert.ok(html.includes('this checkpoint is missing in record (no checkpoint_listed entry for it)'),'PD-7: what the record lacks is shown');
  assert.ok(html.includes('not listed: the run record lists only the checkpoints the App recognizes (CE-1)'),'an invalid checkpoint is not listed');
  assert.ok(!html.includes('No arrival recorded in this run'),'no arrival reading without a listing');
  assert.ok(html.includes('the act is recorded only when you perform it'));
  assert.ok(html.includes('present, currently unavailable: host reported unavailable'),'a runtime unavailability is a requirement outcome, not a hold');
  assert.ok(!FORBIDDEN.test(html),html.match(FORBIDDEN)?.[0]);
  assert.equal(arrivalLabel('waiting'),'reached; act not yet recorded');
  assert.equal(arrivalLabel('held'),'not a recorded disposition (held)');
  assert.deepEqual(['A4','A5','A6','A7','A12'].map(actLabel),['mark checked','accept','approve','rely','set grant']);
});

// The run view's records as the host reports them (runtime_session WorkflowRun::view), with bodies.
const entry=(kind,body,over={})=>({kind,recordId:`${kind}-${JSON.stringify(body).length}`,observedAt:'t',written:true,limit:null,body,...over});
const listedCheck=entry('checkpoint_listed',{checkpoint:'CP-check',requiredAct:'A4',reachedWhenKind:'output_produced',subjectClass:'objects changed by named outcome',governed:false,purpose:'p',scope:'s',
  evaluability:{status:'evaluable with limit',reason:'AW-6: a completed agent message whose first non-empty line is exactly "## Examination report — supports-adjust".'}});
const listedAccept=entry('checkpoint_listed',{checkpoint:'CP-accept',requiredAct:'A5',reachedWhenKind:'host_outcome',subjectClass:'change items of named proposal',governed:false,purpose:'p',scope:'s',
  evaluability:{status:'not evaluable',reason:'Host outcomes (AW-8…AW-10) need a host-supplied mapping or host reads this App does not have. No arrival will be recorded.'}});
const arrival=(checkpoint,ordinal,ref,subject,over={})=>entry('checkpoint_arrival',{checkpoint,requiredAct:'A4',subjectClass:'named output',governed:false,arrivalOrdinal:ordinal,
  event:{source:'native_item',ref,evidencedTime:{value:'2026-09-21T14:13:20.123Z',source:'supplier_item_time'}},
  referents:[{subject,content:{method:'chirality.app.exact-bytes.sha256/v1',value:'0123456789abcdef0123',scope:'text'}}],purpose:'p',scope:'s',
  limits:['The designating line marks where the agent put the output; it does not show that the content is what the declaration describes (AW-6).'],requestObservation:{state:'not yet observed'}},over);
const disposition=(checkpoint,ordinal,d)=>entry('disposition_change',{arrival:{checkpoint,arrivalOrdinal:ordinal},disposition:d,annotations:[]});

test('recorded arrivals are shown from the run record, as information that holds nothing (CE-1, CE-3, CE-12, SD-2)',()=>{
  const a=arrival('CP-check',1,'item:thread/turn/m1','objects changed by named outcome (examination-report)');
  const records=[entry('run_opened',{}),listedAccept,listedCheck,a,disposition('CP-check',1,'waiting'),
    entry('continued_past',{arrival:{checkpoint:'CP-check',arrivalOrdinal:1},actionRef:'item:thread/turn/c1',actKind:'A4'},{written:false,limit:'run record write failed: Not a directory'})];
  const html=h(RunPanel,{run:run({lifecycle:{state:'open',records}})});
  assert.ok(html.includes('aria-label="Recorded arrivals of CP-check"'));
  assert.ok(html.includes('Arrival 1: reached; act not yet recorded. Observed item:thread/turn/m1 at 2026-09-21T14:13:20.123Z (time Codex gave for the item).'));
  assert.ok(html.includes('Request for the act: no request from the agent observed.'));
  assert.ok(html.includes('The agent went on with item:thread/turn/c1 with no act recorded against this arrival. This is a record, not a finding against the agent.'));
  assert.ok(html.includes('Limit: The designating line marks where the agent put the output'));
  assert.ok(html.includes('listed. The App records an arrival only from what it observes in the conversation: AW-6'));
  assert.ok(html.includes('listed. The App does not record arrivals for it: Host outcomes (AW-8…AW-10)'),'a non-evaluable checkpoint says so');
  // A-12 / CE-19: the entry that could not be written is visible on the run.
  assert.ok(html.includes('role="alert">1 run record entry is not yet written (continued_past): run record write failed: Not a directory.'));
  assert.ok(html.includes('If the App quits first they are lost.'));
  assert.ok(!FORBIDDEN.test(html),html.match(FORBIDDEN)?.[0]);
  const shown=html.slice(html.indexOf('aria-label="Recorded arrivals of CP-check"'));const list=shown.slice(0,shown.indexOf('</ul>'));
  assert.ok(list.includes('Arrival 1')&&!/\bchecked\b|verified|approved|accepted|relied|performed|passed/i.test(list),`an arrival infers no act: ${list}`);
  assert.equal(h(RecordWriteNotice,{run:run()}),'','no notice while everything is written');
  // An arrival written late carries its CE-19 limit.
  const late=[...records.slice(0,5),entry('evidence_limit',{label:'record write failed',subjectRef:a.recordId})];
  assert.ok(h(RunPanel,{run:run({lifecycle:{state:'open',records:late}})}).includes('Written late; the run record carries a “record write failed” limit for it.'));
  // On the live run the host marks the entry itself (the limit entry is not in its view).
  const live=[...records.slice(0,3),{...a,writtenLate:true,limit:'run record write failed: Not a directory'},disposition('CP-check',1,'waiting')];
  assert.ok(h(RunPanel,{run:run({lifecycle:{state:'open',records:live}})}).includes('Written late; the run record carries a “record write failed” limit for it.'));
  // Listed with no arrival yet.
  const quiet=h(RunPanel,{run:run({lifecycle:{state:'open',records:[entry('run_opened',{}),listedAccept,listedCheck]}})});
  assert.ok(quiet.includes('No arrival recorded in this run.'));
});

test('counted and not-counted acts, requests, declines and declaration findings are shown from the record (CE-2, CE-4…CE-6, CE-8)',()=>{
  const a=arrival('CP-rely',1,'item:thread/turn/f1','output summary: file out/summary.md');
  const at={checkpoint:'CP-rely',arrivalOrdinal:1};
  const act=(id,kind,time)=>({recordId:id,actKind:kind,capturedAt:time,capturingSurface:'app_act_control'});
  const all=[a,disposition('CP-rely',1,'waiting'),
    entry('act_request',{requester:{kind:'agent'},form:'supplier person-input request',actKind:'not named by the request',subject:'not named by the request',purpose:'not named by the request',association:'associated with the current arrival',arrival:at,evidence:{kind:'conversation item',ref:'server-request:1/2',resolutionAtWrite:'resolved'},time:'t'}),
    entry('act_not_counted',{arrival:at,act:act('rec:app:old','A7','2026-09-21T13:00:00.000Z'),reason:'content no longer current',capturedBeforeArrival:true}),
    entry('act_counted',{arrival:at,act:act('rec:app:rely','A7','2026-09-21T15:00:00.000Z'),relation:'after arrival',referents:['output summary: file out/summary.md']}),
    disposition('CP-rely',1,'performed')];
  const html=h(ArrivalRecord,{arrival:a,all});
  assert.ok(html.includes('Arrival 1: performed.'),html);
  assert.ok(html.includes('Request for the act observed: supplier person-input request from agent; act kind not named by the request. A request is not the act.'));
  assert.ok(!html.includes('no request from the agent observed'));
  assert.ok(html.includes('Act not counted: A7 rec:app:old, captured 2026-09-21T13:00:00.000Z: content no longer current (prior act not counted).'));
  assert.ok(html.includes('Act counted: A7 rec:app:rely, captured 2026-09-21T15:00:00.000Z in the App act control, after the arrival.'));
  const declined=h(ArrivalRecord,{arrival:a,all:[a,entry('arrival_declined',{arrival:at,declinedEventRef:'rec:app:no'}),disposition('CP-rely',1,'resolved negatively')]});
  assert.ok(declined.includes('Arrival 1: resolved negatively.')&&declined.includes('Declined by the person (rec:app:no).'));
  const element={value:{...raw.checkpoints[0],name:'CP-bad',required_act:'A3'},reading:'invalid',findings:['FB-03: recognized act not permitted as checkpoint']};
  const finding=entry('declaration_finding',{checkpoint:'CP-bad',finding:'invalid',code:'FB-03'});
  const guidance=h(CheckpointGuidance,{element,run:run({lifecycle:{state:'open',records:[entry('run_opened',{}),finding]}})});
  assert.ok(guidance.includes('not listed: reported as a declaration finding (invalid, FB-03); no arrival is recorded for it (CE-2).'),guidance);
});

test('recorded lapses are shown against the arrival, and nothing is held because of them (CE-10, RC-8, SD-2)',()=>{
  const a=arrival('CP-rely',1,'item:thread/turn/f1','output summary: file out/summary.md');
  const at={checkpoint:'CP-rely',arrivalOrdinal:1};
  const act={recordId:'rec:app:rely',actKind:'A7',capturedAt:'2026-09-21T15:00:00.000Z',capturingSurface:'app_act_control'};
  const c0={method:'chirality.app.exact-bytes.sha256/v1',value:'00'},c1={method:'chirality.app.exact-bytes.sha256/v1',value:'11'};
  const lapse=(state,when,time,over={})=>entry('act_lapsed',{act,state,referents:['/p/out/summary.md'],c0,c1,time,arrival:at,when,...over});
  const before=[a,entry('act_counted',{arrival:at,act,relation:'after arrival',referents:['output summary: file out/summary.md']}),disposition('CP-rely',1,'performed'),
    lapse('lapsed','before resume','2026-09-21T16:00:00.000Z'),disposition('CP-rely',1,'waiting')];
  const html=h(ArrivalRecord,{arrival:a,all:before});
  assert.ok(html.includes('Arrival 1: reached; act not yet recorded.'),html);
  assert.ok(html.includes('Lapse observed for A7 rec:app:rely at 2026-09-21T16:00:00.000Z (before resume): the file&#x27;s content changed. Lapsed at 2026-09-21T16:00:00.000Z; the arrival is recorded as waiting again. Nothing is asked or stopped because of it.'),html);
  const after=h(ArrivalRecord,{arrival:a,all:[...before.slice(0,3),lapse('lapsed','after resume','2026-09-21T17:00:00.000Z'),disposition('CP-rely',1,'performed'),
    lapse('unknown (unavailable)','after resume','2026-09-21T17:30:00.000Z',{c1:{notObtainable:true,reason:'not a regular file'}})]});
  assert.ok(after.includes('Arrival 1: performed.')&&after.includes('Act lapsed at 2026-09-21T17:00:00.000Z; the arrival stays performed.'),after);
  assert.ok(after.includes('(after resume): lapse unknown: the file could not be read. Nothing is asked'),after);
  assert.ok(!FORBIDDEN.test(html+after),(html+after).match(FORBIDDEN)?.[0]);
});

test('an arrival bound to an output is evidence of where it was put, never a standing',()=>{
  const output={name:'summary',promised_standing:[]};
  const bound=[entry('run_opened',{}),listedCheck,arrival('CP-sum',1,'item:thread/turn/m2','output summary: agentMessage m2'),disposition('CP-sum',1,'waiting')];
  const facets=outputStanding(output,run({lifecycle:{state:'open',records:bound}}));
  assert.equal(facets.evidence,'observed in the conversation only: item:thread/turn/m2 (arrival of CP-sum). That marks where the agent put the output; it does not show that its content meets the declaration');
  assert.equal(facets.humanActs,'none recorded in this run (acts on App files are in their own act log)');
  assert.equal(facets.hostChecks,'none reported');
  // Another output keeps "missing"; a disposition other than waiting, or an unreadable body, reads unknown.
  assert.ok(outputStanding({name:'examination-report'},run({lifecycle:{state:'open',records:bound}})).evidence.startsWith('missing'));
  // An act-related label at an arrival bound to an output that declares no gating checkpoint:
  // its human-act facet is unknown; the other facets keep their rules (AS §8).
  const performed=outputStanding(output,run({lifecycle:{state:'open',records:[...bound,disposition('CP-sum',1,'performed')]}}));
  assert.ok(performed.humanActs.startsWith('unknown: acts are recorded at an arrival bound to summary, which declares no gating checkpoint'),performed.humanActs);
  assert.equal(performed.hostChecks,'none reported');assert.ok(performed.evidence.startsWith('observed in the conversation only'));
  const bodiless=outputStanding(output,run({lifecycle:{state:'open',records:record(['run_opened','checkpoint_arrival'])}}));
  assert.ok(Object.values(bodiless).every(v=>v.startsWith('unknown')));
});

test('an output gated by a checkpoint shows that checkpoint’s act standing from the record (AS §8 Human acts, OV-5)',()=>{
  const gated={name:'summary',form:'file',gating_checkpoint:'CP-rely',promised_standing:['relied on by the person']};
  const at={checkpoint:'CP-rely',arrivalOrdinal:1};
  const act=(id,time)=>({recordId:id,actKind:'A7',capturedAt:time,capturingSurface:'app_act_control'});
  const c0={method:'chirality.app.exact-bytes.sha256/v1',value:'00000000000000aa'},c1={method:'chirality.app.exact-bytes.sha256/v1',value:'11'};
  const a=arrival('CP-rely',1,'item:thread/turn/f1','output summary: file out/summary.md');
  const counted=(id,time,relation='after arrival')=>entry('act_counted',{arrival:at,act:act(id,time),relation,referents:['output summary: file out/summary.md']});
  const performed=(ids,ordinal=1,annotations=[])=>entry('disposition_change',{arrival:at,disposition:'performed',performanceOrdinal:ordinal,answeredBy:ids,annotations});
  const lapse=(state,time,over={})=>entry('act_lapsed',{act:act('rec:app:rely','T1'),state,referents:['/p/out/summary.md'],c0,c1,time,arrival:at,when:'after resume',...over});
  const facet=records=>outputStanding(gated,run({lifecycle:{state:'open',records:[entry('run_opened',{}),...records]}}));
  const base=[a,disposition('CP-rely',1,'waiting'),counted('rec:app:rely','T1'),performed(['rec:app:rely'])];
  // Counted, no lapse recorded: never "not lapsed" (not yet evaluated is never shown as not lapsed).
  const f=facet(base);
  assert.equal(f.humanActs,'checkpoint CP-rely, arrival 1: performed (performance 1); A7 rec:app:rely, captured T1; lapse: not yet evaluated (no lapse observation recorded; not shown as not lapsed). Actor, recorder and recording mode are in the act record, not in the run record.');
  assert.equal(f.hostChecks,'none reported','the other facets keep their rules');assert.equal(f.temporal,'unknown: no result for this output is recorded');
  // By earlier act.
  assert.ok(facet([a,disposition('CP-rely',1,'waiting'),counted('rec:app:rely','T0','earlier act'),performed(['rec:app:rely'])]).humanActs.includes('A7 rec:app:rely, captured T0 — by earlier act rec:app:rely at T0;'));
  // Not counted: prior act not counted before the arrival; after it, the recorded reason.
  const waitingOnly=facet([a,disposition('CP-rely',1,'waiting'),entry('act_not_counted',{arrival:at,act:act('rec:app:old','T0'),reason:'content no longer current',capturedBeforeArrival:true}),
    entry('act_not_counted',{arrival:at,act:act('rec:app:other','T2'),reason:'act on other content',capturedBeforeArrival:false}),disposition('CP-rely',1,'waiting')]).humanActs;
  assert.equal(waitingOnly,'checkpoint CP-rely, arrival 1: reached; no act recorded for it. Not counted: A7 rec:app:old, captured T0: prior act not counted — content no longer current; A7 rec:app:other, captured T2: act not counted — act on other content.');
  // Lapsed (after resume: still performed), with c₀; subject absent; matches c₀ again; unknown states.
  const lapsed=facet([...base,lapse('lapsed','T3'),performed(['rec:app:rely'],1,[{label:'act lapsed at',time:'T3'}])]).humanActs;
  assert.ok(lapsed.includes('performed (performance 1)')&&lapsed.includes('lapse: lapsed (observed T3; c₀ chirality.app.exact-bytes.sha256/v1 000000000000)'),lapsed);
  assert.ok(facet([...base,lapse('lapsed (subject absent)','T3',{c1:'subject absent',when:'before resume'}),disposition('CP-rely',1,'waiting')]).humanActs
    .includes('reached again; the act on its current content is not yet recorded (performance 1); A7 rec:app:rely, captured T1; lapse: lapsed (subject absent) (observed T3'));
  assert.ok(facet([...base,lapse('lapsed','T3'),lapse('matches c0 again after observed lapse','T4',{c1:c0})]).humanActs.includes('lapse: matches c₀ again after observed lapse (observed T4'));
  for(const state of ['unknown (incomparable)','unknown (unavailable)']){
    const u=facet([...base,lapse('lapsed','T3'),lapse(state,'T5',{c1:{notObtainable:true,reason:'x'}})]).humanActs;
    assert.ok(u.includes(`lapse: ${state} (observed T5)`),u);assert.ok(!u.includes('lapse: lapsed'),'the latest observation, unknown, is shown');
  }
  // A new performance after a lapse: its own act, ordinal 2.
  const again=facet([...base,lapse('lapsed','T3',{when:'before resume'}),disposition('CP-rely',1,'waiting'),counted('rec:app:next','T6'),performed(['rec:app:next'],2)]).humanActs;
  assert.ok(again.includes('performed (performance 2); A7 rec:app:next, captured T6; lapse: not yet evaluated'),again);
  // Declined; joint answer; no arrival; an unknown disposition.
  assert.ok(facet([a,entry('arrival_declined',{arrival:at,declinedEventRef:'rec:app:no'}),disposition('CP-rely',1,'resolved negatively')]).humanActs.includes('resolved negatively — declined (rec:app:no)'));
  assert.ok(facet([...base.slice(0,3),counted('rec:app:two','T2'),performed(['rec:app:rely','rec:app:two'])]).humanActs.includes('answered by 2 acts: '));
  assert.equal(facet([]).humanActs,'none recorded in this run: checkpoint CP-rely, which gates this output, has no recorded arrival');
  assert.ok(facet([a,disposition('CP-rely',1,'unknown')]).humanActs.startsWith('unknown'));
  // A loss, deciding or not: the record holds an entry this view does not read; every facet stays unknown.
  for(const deciding of [true,false]){
    const lost=facet([...base,entry('observation_lost',{scope:'s',cause:'c',deciding})]);
    assert.ok(Object.values(lost).every(v=>v.startsWith('unknown')),JSON.stringify(lost));
  }
  // An output gated by another checkpoint is not given this checkpoint's act.
  assert.ok(outputStanding({...gated,gating_checkpoint:'CP-check'},run({lifecycle:{state:'open',records:base}})).humanActs.startsWith('none recorded in this run: checkpoint CP-check'));
  // M-1 (PH-4, RC-2): never "performed" without the act: a label citing an act with no
  // act_counted entry at this arrival, or citing none, is unknown with the reason.
  const ghost=facet([a,disposition('CP-rely',1,'waiting'),performed(['rec:app:ghost'])]).humanActs;
  assert.equal(ghost,'unknown: checkpoint CP-rely, arrival 1 is labelled performed but no act_counted entry at this arrival cites rec:app:ghost');
  assert.equal(facet([a,disposition('CP-rely',1,'waiting'),performed([])]).humanActs,'unknown: checkpoint CP-rely, arrival 1 is labelled performed but the label names no act');
  const elsewhere=entry('act_counted',{arrival:{checkpoint:'CP-rely',arrivalOrdinal:2},act:act('rec:app:rely','T1'),relation:'after arrival',referents:[]});
  assert.ok(facet([a,disposition('CP-rely',1,'waiting'),elsewhere,performed(['rec:app:rely'])]).humanActs.startsWith('unknown'),'an act counted at another arrival does not answer this one');
  // M-2: a body missing a field its kind requires is unreadable: every facet unknown.
  const malformed=[
    entry('act_counted',{arrival:at,act:{actKind:'A7',capturedAt:'T1',capturingSurface:'app_act_control'},relation:'after arrival',referents:[]}),
    entry('act_counted',{arrival:at,act:act('rec:app:rely','T1'),referents:[]}),
    entry('act_not_counted',{arrival:at,act:act('rec:app:old','T0'),capturedBeforeArrival:true}),
    entry('act_lapsed',{act:act('rec:app:rely','T1'),referents:['/p'],c0,c1,arrival:at,when:'after resume'}),
    entry('act_lapsed',{act:act('rec:app:rely','T1'),state:'lapsed',referents:['/p'],c1,time:'T3',arrival:at}),
    entry('arrival_declined',{arrival:at}),
    entry('run_resumed',{arrival:at,time:'T2'}),
    entry('disposition_change',{arrival:at,disposition:'performed',performanceOrdinal:0,answeredBy:['rec:app:rely']}),
    entry('disposition_change',{arrival:at,disposition:'performed',performanceOrdinal:1,answeredBy:'rec:app:rely'}),
    entry('disposition_change',{arrival:at,disposition:'held'}),
    entry('act_counted',{arrival:{checkpoint:'CP-rely',arrivalOrdinal:'1'},act:act('rec:app:rely','T1'),relation:'after arrival',referents:[]}),
  ];
  for(const bad of malformed){
    const f=facet([...base,bad]);
    assert.ok(Object.values(f).every(v=>v.startsWith('unknown')),`${JSON.stringify(bad.body)}: ${JSON.stringify(f)}`);
  }
  // Ungated, with no arrival bound to it: "none recorded for this output".
  assert.equal(outputStanding({name:'other-output'},run({lifecycle:{state:'open',records:[entry('run_opened',{}),...base]}})).humanActs,'none recorded for this output (acts on App files are in their own act log)');
  const html=h(StandingFacets,{facets:f});
  assert.ok(!/\bchecked\b|verified|approved|accepted|relied|passed|not lapsed\)/i.test(html.replace('not shown as not lapsed','')),html);
  assert.ok(!FORBIDDEN.test(html));
});

test('standing facets show only what the run record supports',()=>{
  const output={name:'resolution-report',promised_standing:['host checks passed: spacing']};
  const facets=outputStanding(output,run());
  assert.deepEqual(facets,{temporal:'unknown: no result for this output is recorded',hostChecks:'none reported',limitations:'none reported',
    humanActs:'none recorded for this output (acts on App files are in their own act log)',examination:'none recorded',
    evidence:'missing: no record of resolution-report in the run record',route:'not recorded'});
  // A record holding entries this view does not read makes the facets unknown, never stronger.
  const withActs=outputStanding(output,run({lifecycle:{state:'open',records:record(['run_opened','human_act','examination_findings'])}}));
  assert.ok(Object.values(withActs).every(v=>v.startsWith('unknown')),JSON.stringify(withActs));
  // Only kinds known to say nothing about outputs leave "none recorded"; any other kind, including future ones, reads unknown.
  for(const kind of ['act_counted','act_lapsed','item_decision','continued_past','observation_lost','evidence_limit','operation_entry','a_kind_not_yet_defined']){
    const f=outputStanding(output,run({lifecycle:{state:'open',records:record(['run_opened',kind])}}));
    assert.ok(Object.values(f).every(v=>v.startsWith('unknown')),`${kind}: ${JSON.stringify(f)}`);
  }
  const neutral=outputStanding(output,run({lifecycle:{state:'ended',records:record(['run_opened','supplied_guidance','compatibility_report_ref','run_ended'])}}));
  assert.equal(neutral.hostChecks,'none reported');
  const html=h(StandingFacets,{facets});
  assert.ok(!/\bchecked\b|verified|approved|accepted|relied|passed/i.test(html),'no checking, acceptance or reliance is inferred');
  const panel=h(RunPanel,{run:run()});
  assert.ok(panel.includes('Declared promise, not a standing:'),'the promise is labelled apart from the standing');
  assert.ok(panel.includes('Run record entries: run_opened, supplied_guidance.'));
});

test('a role outside the written-for roles is shown with the way to another role (U-R10)',()=>{
  const doc={...raw,compatible_roles:['HELP_HUMAN']};
  const entry={...run().compatibility[0],preparation:{...run().compatibility[0].preparation,declaration:declaration(doc),
    check:{result:'unsupported',tools:[],findings:['workflow is written for ["HELP_HUMAN"]; role in force WORKING_ITEMS']}}};
  const html=h(CompatibilityAdvisory,{entry});
  assert.ok(html.includes('requirement check does not pass'));
  assert.ok(html.includes('The workflow is written for HELP_HUMAN; this conversation has WORKING_ITEMS.'));
  assert.ok(html.includes('You may still start or continue the run.')&&html.includes('use Continue as on the conversation'));
  assert.ok(html.includes('Advisory: it never decides whether the run starts.'));
  assert.ok(!html.includes('Finding: workflow is written for'),'the role finding is shown once');
  const none=h(CompatibilityAdvisory,{entry:{...entry,preparation:{...entry.preparation,role:{standing:'unknown',reason:'original App supply binding not established'}}}});
  assert.ok(none.includes('Role in force: not established (original App supply binding not established)'));
  assert.ok(!none.includes('this conversation has'),'an unknown role is not read as a mismatch');
  assert.ok(!FORBIDDEN.test(html+none));
});

test('the selected workflow shows its declared part instead of a JSON dump',async()=>{
  const html=h(SelectedWorkflow,{selection:{identity:{name:'resolve-spacing',origin:'project',revision:'0123456789abcdef'},standing:'registered',runnable:true,declaration:declaration()}});
  assert.ok(html.includes('Selected: <b>resolve-spacing</b> (project), revision 0123456789ab'));
  assert.ok(html.includes('<b>CP-accept</b>'));
  assert.ok(h(SelectedWorkflow,{selection:{state:'not-selected'}}).includes('No workflow selected.'));
  assert.ok(h(DeclaredPart,{declaration:{unavailable:'workflow text unreadable'}}).includes('Declared part could not be read: workflow text unreadable'));
  const undeclared=h(DeclaredPart,{declaration:{raw:null,reading:'undeclared',categories:Object.fromEntries(cats.map(c=>[c,'undeclared'])),elements:{},findings:[]}});
  assert.ok(undeclared.includes('declares no requirements part')&&undeclared.includes('Not declared.'));
  const {installMiniDom}=await import('./support/mini-dom.mjs');
  const document=installMiniDom();const {createRoot}=await import('react-dom/client');
  const {WorkflowRootPanel}=load('App.tsx');
  const g={appSession:'selected-workflow-session',home:'selected-workflow-home',spawnCounter:1};
  const conversations=['chat-a','chat-b'].map(threadId=>({generation:g,threadId}));
  const declared=purpose=>{const doc=structuredClone(raw);doc.checkpoints[0].purpose=purpose;return declaration(doc);};
  const choice=(reference,name,purpose)=>({reference,identity:{name,origin:'project',revision:'0123456789abcdef'},standing:'registered',runnable:true,declaration:declared(purpose)});
  const original=run({reference:'run-original',conversation:'chat-b',workflow:{...run().workflow,name:'original-running-workflow'},
    compatibility:[{...run().compatibility[0],preparation:{...run().compatibility[0].preparation,declaration:declared('Original run checkpoint purpose')}}]});
  const data={context:{sourceRef:'workflow-source',generation:g,historyEpoch:1},
    inspection:choice('inspection','inspected-workflow','Inspected checkpoint purpose'),
    selections:[{sourceRef:'workflow-source',threadId:'chat-a',selection:choice('choice-a','selected-workflow-a','Selected A checkpoint purpose')},
      {sourceRef:'workflow-source',threadId:'chat-b',selection:choice('choice-b','selected-workflow-b','Selected B checkpoint purpose')}],
    runs:[original],runBringBackDefaults:[{run:original.reference,threadId:'chat-a'}]};
  const host={state:'ready',generation:g,threads:conversations,workflowRoot:data};
  const calls=[];const act=async(command,args)=>{calls.push([command,args]);return {state:'pre-filled; not sent'};};
  const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
  const props=node=>node[Object.keys(node).find(key=>key.startsWith('__reactProps$'))];
  const labelled=name=>container.querySelectorAll(node=>node.getAttribute('aria-label')===name)[0];
  const selectIn=(parent,label)=>parent.querySelectorAll(node=>node.localName==='label'&&node.textContent.startsWith(label))[0].querySelectorAll(node=>node.localName==='select')[0];
  const render=async(fileActBusy=false)=>React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data,host,act,fileActBusy})));
  try{
    await render();
    assert.match(labelled('Inspected workflow content').textContent,/inspected-workflow.*Inspected checkpoint purpose/s);
    assert.equal(labelled('Selected workflow'),undefined,'inspection does not silently select for a conversation');
    const chat=selectIn(container,'Workflow chat ');
    await React.act(()=>props(chat).onChange({target:{value:'chat-a'}}));
    assert.match(labelled('Selected workflow').textContent,/selected-workflow-a.*Selected A checkpoint purpose/s);
    assert.doesNotMatch(labelled('Selected workflow').textContent,/Selected B checkpoint purpose|Inspected checkpoint purpose/);
    const originalPanel=labelled('Run panel');
    assert.match(originalPanel.textContent,/original-running-workflow.*conversation chat-b.*Original run checkpoint purpose/s);
    assert.doesNotMatch(originalPanel.textContent,/Selected A checkpoint purpose/,'the run keeps its own declaration');
    await React.act(()=>props(chat).onChange({target:{value:'chat-b'}}));
    assert.match(labelled('Selected workflow').textContent,/selected-workflow-b.*Selected B checkpoint purpose/s);
    assert.doesNotMatch(labelled('Selected workflow').textContent,/Selected A checkpoint purpose/);
    assert.match(originalPanel.textContent,/Original run checkpoint purpose/,'changing the selected chat does not rebind a started run');
    await React.act(()=>props(chat).onChange({target:{value:'chat-a'}}));
    const target=selectIn(originalPanel,'Bring back to ');
    await React.act(()=>props(target).onChange({target:{value:JSON.stringify([g,'chat-b'])}}));
    const bringBack=()=>originalPanel.querySelectorAll(node=>node.localName==='button'&&node.textContent==='Bring a real run back to authoring')[0];
    assert.deepEqual(calls,[],'rendering declarations and changing interface choices calls no host action');
    await render(true);
    assert.equal(props(bringBack()).disabled,true,'the shared file-act operation disables run actions through the actual wiring');
    assert.deepEqual(calls,[]);
    await render(false);
    assert.equal(props(bringBack()).disabled,false);
    await React.act(async()=>{await props(bringBack()).onClick();});
    assert.deepEqual(calls,[['workflow_run_bring_back',{runRef:original.reference,generation:g,threadId:'chat-b',includeNative:false}]],'only the explicit press names the original run and the separately chosen current target');
  }finally{await React.act(()=>root.unmount());document.body.removeChild(container);}
});

test('Bring a real run back to authoring calls the host only on the press, with the chosen conversation (TT-10, TT-11)',()=>{
  const g={appSession:'s',home:'h',spawnCounter:1};
  const conversations=[{generation:g,threadId:'auth'},{generation:g,threadId:'other'}];
  const calls=[];const act=async(c,a)=>{calls.push([c,a]);};
  const find=(node,found=[])=>{if(Array.isArray(node)){for(const n of node)find(n,found);return found;}if(!node||typeof node!=='object')return found;if(typeof node.type==='function')return find(node.type(node.props),found);if(node.type==='button')found.push(node);find(node.props?.children,found);return found;};
  const view=(target,includeNative=false)=>RunBringBackView({run:run(),conversations,target,setTarget:()=>{},includeNative,setIncludeNative:()=>{},busy:false,act});
  assert.equal(find(view(''))[0].props.disabled,true,'no conversation chosen, no bring back');
  assert.deepEqual(calls,[]);
  find(view(JSON.stringify([g,'other']),true))[0].props.onClick();
  assert.deepEqual(calls,[['workflow_run_bring_back',{runRef:'run-1',generation:g,threadId:'other',includeNative:true}]]);
  assert.ok(h(RunPanel,{run:run(),conversations,act}).includes('Bring a real run back to authoring'));
  assert.ok(!h(RunPanel,{run:run()}).includes('Bring a real run back'),'offered only where the host can be asked');
});

test('reopened run learning keeps its recorded standing and uses only the chosen current target on an explicit press',()=>{
  const g={appSession:'current',home:'target-home',spawnCounter:2};
  const conversations=[{generation:g,threadId:'target'}];
  const recorded={run:'run:historical',conversation:'original-source',state:'ended',workflow:{origin:'project',name:'resolve-spacing',revision:'abcdef0123456789'},
    learning:{bringBack:{offered:true},compare:{offered:true},standing:'Unsigned recorded evidence; source home resolved separately; no live run restored.'}};
  const calls=[];
  const props={run:recorded,conversations,target:JSON.stringify([g,'target']),setTarget:()=>{},includeNative:false,setIncludeNative:()=>{},busy:false,act:async(c,a)=>calls.push([c,a])};
  const tree=RunBringBackView(props);
  const buttons=node=>{if(Array.isArray(node))return node.flatMap(buttons);if(!node||typeof node!=='object')return [];return [...(node.type==='button'?[node]:[]),...buttons(node.props?.children)];};
  assert.deepEqual(calls,[],'rendering performs no native history read or send');
  assert.equal(buttons(tree)[0].props.disabled,false);
  assert.match(renderToStaticMarkup(tree),/Unsigned recorded evidence/);
  assert.match(renderToStaticMarkup(tree),/Recorded evidence \(unsigned\)/);
  buttons(tree)[0].props.onClick();
  assert.deepEqual(calls,[['workflow_run_bring_back',{runRef:'run:historical',generation:g,threadId:'target',includeNative:false}]],'the renderer supplies no historical source home or path');
  const unavailable=RunBringBackView({...props,run:{...recorded,learning:{...recorded.learning,bringBack:{offered:false,reason:'Original recorded source home is not available in this App.'}}}});
  assert.equal(buttons(unavailable)[0].props.disabled,true);
  assert.match(renderToStaticMarkup(unavailable),/Bring back is unavailable: Original recorded source home/);
  const unread=RunBringBackView({...props,run:{...recorded,learning:undefined}});
  assert.equal(buttons(unread)[0].props.disabled,true);
  assert.match(renderToStaticMarkup(unread),/Reopen the recorded runs/);
});

test('the reopened workspace offers learning without original-send or live-run controls, while a live sent run retains its controls',()=>{
  const {WorkflowRootPanel}=load('App.tsx');
  const g={appSession:'current',home:'h',spawnCounter:1};
  const conversations=[{generation:g,threadId:'auth'}];
  const calls=[];const act=async(c,a)=>calls.push([c,a]);
  const historical={run:'run:old',conversation:'original',state:'ended',workflow:run().workflow,
    learning:{bringBack:{offered:true},compare:{offered:true},standing:'Unsigned recorded run evidence; no live authority restored.'}};
  const old=h(WorkflowRootPanel,{data:{runs:[],reopened:{runs:[historical],standing:'Recorded lifecycle only.'}},host:{state:'ready',generation:g,threads:conversations},act});
  assert.match(old,/Bring a real run back to authoring/);
  assert.match(old,/Unsigned recorded run evidence/);
  assert.doesNotMatch(old,/Record, then send original prepared text once|Check original native supplied text pages|>End run<|End this run and start/);
  const live=h(WorkflowRootPanel,{data:{runs:[run({source:{kind:'actual native turn source'},turn:'turn:live',endNotice:{state:'pending'},pendingRecords:true})]},host:{state:'ready',generation:g,threads:conversations},act});
  assert.match(live,/Check original native supplied text pages/);
  assert.match(live,/>End run<|>End run<\/button>/);
  assert.match(live,/Retry pending records/);
  assert.match(live,/The next message in this conversation/);
  assert.doesNotMatch(live,/Reopen the recorded runs to establish/,'native source evidence does not make a live owner historical');
  assert.deepEqual(calls,[]);
});

test('a native send with an unsaved history reference enables record-only retry without losing its live controls or resending',async()=>{
  const {installMiniDom}=await import('./support/mini-dom.mjs');
  const document=installMiniDom();const {createRoot}=await import('react-dom/client');
  const {WorkflowRootPanel}=load('App.tsx');
  const g={appSession:'current',home:'h',spawnCounter:1};
  const pointer={originalText:'wr-record:v1:original',purpose:'run start',persistence:'memory-only',limit:'fixture metadata save failure',standing:'acknowledgment pointer only'};
  const live=run({source:{kind:'actual native turn source'},turn:'native:started',status:{state:'native response observed'},pendingRecords:false,learningPointers:[pointer]});
  const calls=[];const act=async(c,a)=>{calls.push([c,a]);return {state:'records retried; native send unchanged'};};
  const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
  const props=node=>node[Object.keys(node).find(k=>k.startsWith('__reactProps$'))];
  const button=name=>container.querySelectorAll(n=>n.localName==='button'&&n.textContent===name)[0];
  const render=async value=>React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data:{runs:[value]},host:{state:'ready',generation:g,threads:[]},act})));
  await render(live);
  assert.deepEqual(calls,[]);
  assert.match(container.textContent,/History reference could not be saved \(run start\)/);
  assert.match(container.textContent,/Send: native response observed/);
  assert.ok(button('End run'),'the persistence failure does not remove the live run controls');
  assert.equal(props(button('Record, then send original prepared text once')).disabled,true,'the acknowledged native send cannot be resent');
  assert.equal(props(button('Retry pending records (never sends)')).disabled,false,'a pointer-only failure is retryable even with no pending run records');
  await React.act(async()=>{await props(button('Retry pending records (never sends)')).onClick();});
  assert.deepEqual(calls,[['workflow_retry_records',{runRef:'run-1'}]],'retry asks only to save records, never to send');
  await render({...live,learningPointers:[{...pointer,persistence:'durable App metadata',limit:null}]});
  assert.equal(props(button('Retry pending records (never sends)')).disabled,true);
  assert.doesNotMatch(container.textContent,/History reference could not be saved/);
  await React.act(()=>root.unmount());
});

test('an acknowledged run with a durable history pointer can still retry its unsaved association, while an unacknowledged preparation cannot',async()=>{
  const {installMiniDom}=await import('./support/mini-dom.mjs');const document=installMiniDom();const {createRoot}=await import('react-dom/client');
  const {WorkflowRootPanel}=load('App.tsx');
  const g={appSession:'current',home:'h',spawnCounter:1};
  const live=run({source:{kind:'actual native turn source'},turn:'native:acknowledged',status:{state:'native response observed'},pendingRecords:false,
    runTag:{persistence:'memory-only'},learningPointers:[{purpose:'run start',persistence:'durable App metadata'}]});
  const calls=[];const act=async(c,a)=>{calls.push([c,a]);return {state:'association retried; native send unchanged'};};
  const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
  const props=node=>node[Object.keys(node).find(k=>k.startsWith('__reactProps$'))];
  const button=name=>container.querySelectorAll(n=>n.localName==='button'&&n.textContent===name)[0];
  const render=async value=>React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data:{runs:[value]},host:{state:'ready',generation:g,threads:[]},act})));
  await render(live);
  assert.match(container.textContent,/History reference could not be saved \(run association\)/);
  assert.match(container.textContent,/Send: native response observed/);
  assert.equal(props(button('Retry pending records (never sends)')).disabled,false);
  await React.act(async()=>{await props(button('Retry pending records (never sends)')).onClick();});
  assert.deepEqual(calls,[['workflow_retry_records',{runRef:'run-1'}]]);
  assert.equal(props(button('Record, then send original prepared text once')).disabled,true);
  await render({...live,runTag:{persistence:'durable App metadata'}});
  assert.equal(props(button('Retry pending records (never sends)')).disabled,true);
  assert.doesNotMatch(container.textContent,/History reference could not be saved/);
  await render({...live,source:null,turn:null,status:{state:'prepared'},runTag:{persistence:'memory-only'}});
  assert.equal(props(button('Retry pending records (never sends)')).disabled,true,'an unacknowledged prepared run does not qualify for association retry');
  assert.doesNotMatch(container.textContent,/History reference could not be saved/);
  await React.act(()=>root.unmount());
});

test('a sent reopened end notice can retry its unsaved history reference without offering to carry or send the notice again',async()=>{
  const {installMiniDom}=await import('./support/mini-dom.mjs');
  const document=installMiniDom();const {createRoot}=await import('react-dom/client');const {WorkflowRootPanel}=load('App.tsx');
  const end={run:'run:old',conversation:'original',endNotice:{state:'sent'},learningPointers:[{purpose:'run end notice',persistence:'memory-only',limit:'fixture metadata save failure'}]};
  const calls=[];const act=async(c,a)=>{calls.push([c,a]);return {endNotice:{state:'sent'}};};
  const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
  await React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data:{endedAfterRelaunch:[end]},host:{state:'ready',generation:{},threads:[]},act})));
  assert.deepEqual(calls,[]);
  assert.match(container.textContent,/History reference could not be saved \(run end notice\)/);
  assert.doesNotMatch(container.textContent,/The next message in conversation original carries this end notice/);
  const retry=container.querySelectorAll(n=>n.localName==='button'&&n.textContent==='Retry saving records (never sends)')[0];assert.ok(retry);
  const props=retry[Object.keys(retry).find(k=>k.startsWith('__reactProps$'))];assert.equal(props.disabled,false);
  await React.act(async()=>{await props.onClick();});
  assert.deepEqual(calls,[['workflow_reopened_notice',{runId:'run:old',action:'retry'}]]);
  await React.act(()=>root.unmount());
});

test('Bring a real run back defaults to the host’s default conversation for that run, still changeable; none without one (I-8, TT-10)',async()=>{
  const g={appSession:'s',home:'h',spawnCounter:1};
  const conversations=[{generation:g,threadId:'auth'},{generation:g,threadId:'other'}];
  const root={runBringBackDefaults:[{run:'run-1',threadId:'other'},{run:'run-2',threadId:'auth'}]};
  assert.equal(runBringBackDefault(root,'run-1'),'other');
  assert.equal(runBringBackDefault(root,'run-9'),null);
  assert.equal(runBringBackDefault({},'run-1'),null);
  assert.equal(runBringBackDefault(undefined,'run-1'),null);
  const selected=html=>html.match(/<option value="([^"]*)" selected="">/)?.[1]??null;
  const panel=defaultThread=>h(RunPanel,{run:run(),conversations,bringBackDefault:defaultThread,act:async()=>{}});
  assert.equal(selected(panel(runBringBackDefault(root,'run-1'))),JSON.stringify([g,'other']).replace(/"/g,'&quot;'),'defaults to the host-named conversation');
  assert.equal(selected(panel(null)),'','no default: none chosen');
  assert.equal(selected(panel('gone')),'','a default that is not a started conversation here is not chosen');
  // Mounted: the default is used, sends nothing by itself, and the person can change it.
  const {installMiniDom}=await import('./support/mini-dom.mjs');
  const document=installMiniDom();
  const {createRoot}=await import('react-dom/client');
  const calls=[];const act=async(c,a)=>{calls.push([c,a]);};
  const container=document.createElement('div');document.body.appendChild(container);
  const rootEl=createRoot(container);
  await React.act(()=>rootEl.render(React.createElement(RunPanel,{run:run(),conversations,bringBackDefault:'other',act})));
  assert.deepEqual(calls,[],'mounting sends nothing');
  // React keeps each element's current props on its node; the mini document has no events.
  const props=node=>node[Object.keys(node).find(k=>k.startsWith('__reactProps$'))];
  const press=async()=>{const b=container.querySelectorAll(n=>n.localName==='button'&&n.textContent==='Bring a real run back to authoring')[0];await React.act(()=>props(b).onClick());};
  await press();
  assert.deepEqual(calls.at(-1),['workflow_run_bring_back',{runRef:'run-1',generation:g,threadId:'other',includeNative:false}]);
  const select=container.querySelectorAll(n=>n.localName==='select')[0];
  await React.act(()=>props(select).onChange({target:{value:JSON.stringify([g,'auth'])}}));
  await press();
  assert.deepEqual(calls.at(-1),['workflow_run_bring_back',{runRef:'run-1',generation:g,threadId:'auth',includeNative:false}],'the person’s choice replaces the default');
  await React.act(()=>props(select).onChange({target:{value:''}}));
  assert.equal(props(container.querySelectorAll(n=>n.localName==='button'&&n.textContent==='Bring a real run back to authoring')[0]).disabled,true,'the person may clear it');
  await React.act(()=>rootEl.unmount());
});

test('tool-permission settlements and model turns feed no facet; a lost acknowledgement adds an unknown to evidence only (AS §2, §3.2, §8, DS-3; RS R5, R13, R11)',()=>{
  const gated={name:'summary',form:'file',gating_checkpoint:'CP-rely',promised_standing:['relied on by the person']};
  const plain={name:'resolution-report',promised_standing:[]};
  const facets=(output,records)=>outputStanding(output,run({lifecycle:{state:'open',records:[entry('run_opened',{}),...records]}}));
  const settled=[
    entry('tool_permission_settlement',{request:'server-request:1/1',settledBy:'the person via interaction',settlement:'answered'}),
    entry('tool_permission_settlement',{request:'server-request:1/2',settledBy:'App named-rule decline',settlement:'declined',ruleName:'deny-network'}),
    entry('tool_permission_settlement',{request:'server-request:1/7',settledBy:'none — ended unanswered',settlement:'ended unanswered (process exit)',context:'App quit',custodyEventRef:'cev:rq04:g:7'}),
  ];
  // Settlements leave every facet exactly as the run without them, for a gated and an ungated output.
  for(const output of [gated,plain]) assert.deepEqual(facets(output,settled),facets(output,[]),output.name);
  assert.ok(facets(gated,settled).humanActs.startsWith('none recorded in this run: checkpoint CP-rely'),'an A14 settlement is never a human act');
  // RS R5 model turns (PR #1302) are shown in the channel status, not here (AS §2, §3.2): no facet changes.
  const turns=[entry('model_turn',{turn:1,requested:'fixture-model',effective:'fixture-model',destinationClass:'local model server',scope:'turn'}),
    entry('model_turn',{requested:'fixture-model',effective:'other-model',reroute:true,scope:'thread'})];
  for(const output of [gated,plain]) assert.deepEqual(facets(output,[...settled,...turns]),facets(output,[]),output.name);
  // A lost acknowledgement: evidence gains an unknown note; nothing else changes, nothing is stronger.
  const lost=entry('evidence_limit',{label:'lost acknowledgement',subjectRef:'server-request:1/1',detail:'never acknowledged'});
  const before=facets(plain,settled),after=facets(plain,[...settled,lost]);
  assert.deepEqual({...after,evidence:before.evidence},before);
  assert.equal(after.evidence,`${before.evidence}; unknown (unobserved outcome, observer: the App): Codex's acknowledgement of a reply written to server-request:1/1 was not observed (lost acknowledgement); its relation to resolution-report is not recorded`);
  // An unreadable settlement, another limit or a limit without its subject still reads unknown everywhere.
  for(const r of [entry('tool_permission_settlement',{request:'server-request:1/3',settledBy:'the App',settlement:'answered'}),entry('model_turn',{requested:'m',effective:'m'}),
    entry('evidence_limit',{label:'record write failed',subjectRef:'r1'}),entry('evidence_limit',{label:'lost acknowledgement'})]){
    const f=facets(plain,[r]);
    assert.ok(Object.values(f).every(v=>v.startsWith('unknown')),JSON.stringify(f));
  }
  const html=h(StandingFacets,{facets:after});
  assert.ok(!/\bchecked\b|verified|approved|accepted|relied|passed|permitted/i.test(html),html);
});

test('post-end A4/A6/A7 observations stay against the ended arrival and never alter its disposition or output facets',()=>{
  const a=arrival('CP-rely',1,'item:end/turn/file','output summary: file out/summary.md');
  const final=entry('disposition_change',{arrival:{checkpoint:'CP-rely',arrivalOrdinal:1},disposition:'waiting',performanceOrdinal:0});
  const observations=['A4','A6','A7'].map((actKind,i)=>entry('act_after_run_end',{arrival:{checkpoint:'CP-rely',arrivalOrdinal:1},act:{recordId:`later-${i}`,actKind,capturedAt:'2026-10-13T14:00:00Z',capturingSurface:'app_act_control'}}));
  const records=[a,final,entry('run_ended',{cause:'ended by the person',waitingArrivals:[{checkpoint:'CP-rely',arrivalOrdinal:1}]}),...observations];
  const html=h(ArrivalRecord,{arrival:a,all:records});
  assert.ok(html.includes('reached; act not yet recorded'));for(const kind of ['A4','A6','A7'])assert.ok(html.includes(`After run end: ${kind}`));
  assert.ok(html.includes('The ended arrival disposition is unchanged.'));
  const out={name:'summary',form:'file',gating_checkpoint:'CP-rely',promised_standing:['relied on by the person']};
  const before=outputStanding(out,run({lifecycle:{records:records.slice(0,3)}}));
  assert.deepEqual(outputStanding(out,run({lifecycle:{records}})),before);
  const pending={...observations[0],written:false,limit:'source unavailable; original observation held'};
  assert.ok(h(ArrivalRecord,{arrival:a,all:[a,final,pending]}).includes('Not yet written to the run record'));
  const other={...observations[0],body:{...observations[0].body,arrival:{checkpoint:'CP-rely',arrivalOrdinal:2}}};
  assert.ok(!h(ArrivalRecord,{arrival:a,all:[a,final,other]}).includes('After run end:'));
});

test('actual host tick DTO presents a post-end observation against its final waiting arrival',()=>{
  const {spawnSync}=createRequire(import.meta.url)('node:child_process');
  const {fileURLToPath}=createRequire(import.meta.url)('node:url');
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','runtime_session::workflow_root_tests::after_run_end_actual_tick_reopen_and_new_run_keep_finality','--','--exact','--nocapture','--test-threads=1'],{cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'}});
  assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const line=proc.stdout.split('\n').find(line=>line.includes('AFTER_END_DTO:'));assert.ok(line);
  const dto=JSON.parse(line.slice(line.indexOf('AFTER_END_DTO:')+'AFTER_END_DTO:'.length));
  const records=dto.afterRunEnd.runs[0].records;const a=records.find(r=>r.kind==='checkpoint_arrival');
  const html=h(ArrivalRecord,{arrival:a,all:records});assert.match(html,/After run end: A7/);assert.match(html,/reached; act not yet recorded/);assert.match(html,/ended arrival disposition is unchanged/);
  assert.equal(records.filter(r=>r.kind==='act_after_run_end').length,1);assert.equal(records.filter(r=>r.kind==='act_counted').length,0);
});

test('actual reopened corrected-arrival DTO preserves CE16 history without assigning it to the corrected subject',()=>{
  const {spawnSync}=createRequire(import.meta.url)('node:child_process');const {fileURLToPath}=createRequire(import.meta.url)('node:url');
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','runtime_session::workflow_root_tests::after_run_end_persisted_observation_is_not_rebound_to_corrected_subject','--','--exact','--nocapture','--test-threads=1'],{cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'}});assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const line=proc.stdout.split('\n').find(line=>line.includes('AFTER_END_CORRECTED_DTO:'));assert.ok(line);const dto=JSON.parse(line.slice(line.indexOf('AFTER_END_CORRECTED_DTO:')+'AFTER_END_CORRECTED_DTO:'.length));
  const records=dto.afterRunEnd.runs[0].records;const corrected=records.find(r=>r.kind==='checkpoint_arrival'&&r.corrects);
  const html=h(ArrivalRecord,{arrival:corrected,all:records});assert.match(html,/out\/new.md/);assert.doesNotMatch(html,/After run end: A7/);assert.match(html,/Post-end subject association not established/);
  const {WorkflowRootPanel}=load('App.tsx');const full=h(WorkflowRootPanel,{data:dto,host:{state:'ready',generation:{},threads:[]},act:async()=>{}});
  assert.doesNotMatch(full,/After run end: A7/);assert.match(full,/Recorded post-end source history/);assert.ok(full.includes('act_after_run_end'),'raw CE16 remains inspectable');assert.match(full,/Post-end subject association not established/);
});

test('actual ended performed-file DTO displays a lapse without reopening or asking for an act',()=>{
  const {spawnSync}=createRequire(import.meta.url)('node:child_process');const {fileURLToPath}=createRequire(import.meta.url)('node:url');
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','runtime_session::workflow_root_tests::after_end_file_lapse_actual_owner_tick_and_cold_reopen_keep_the_closed_source','--','--exact','--nocapture','--test-threads=1'],{cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'}});assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const line=proc.stdout.split('\n').find(line=>line.includes('AFTER_END_LAPSE_DTO:'));assert.ok(line);const dto=JSON.parse(line.slice(line.indexOf('AFTER_END_LAPSE_DTO:')+'AFTER_END_LAPSE_DTO:'.length));
  const records=dto.runs[0].lifecycle.records;const a=records.find(r=>r.kind==='checkpoint_arrival');const html=h(ArrivalRecord,{arrival:a,all:records});
  assert.match(html,/Arrival 1: lapsed/);assert.match(html,/after run end; the arrival is recorded as lapsed/);assert.doesNotMatch(html,/recorded as waiting again/);assert.match(html,/Nothing is asked or stopped/);
  assert.equal(records.filter(r=>r.kind==='run_ended').length,1);assert.equal(records.filter(r=>r.kind==='act_lapsed').length,1);
  const facets=outputStanding({name:'summary',form:'file',gating_checkpoint:a.body.checkpoint,promised_standing:['relied on by the person']},run({lifecycle:{records}}));assert.match(facets.humanActs,/lapsed/);
});

test('actual corrected ended lapse DTO keeps the original observation as history without rebinding its label or output facet',()=>{
  const {spawnSync}=createRequire(import.meta.url)('node:child_process');const {fileURLToPath}=createRequire(import.meta.url)('node:url');
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','runtime_session::workflow_root_tests::after_end_file_lapse_persisted_history_is_not_rebound_to_a_corrected_subject','--','--exact','--nocapture','--test-threads=1'],{cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'}});assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const line=proc.stdout.split('\n').find(line=>line.includes('AFTER_END_LAPSE_CORRECTED_DTO:'));assert.ok(line);const dto=JSON.parse(line.slice(line.indexOf('AFTER_END_LAPSE_CORRECTED_DTO:')+'AFTER_END_LAPSE_CORRECTED_DTO:'.length));const records=dto.afterRunEnd.runs[0].records;const a=records.find(r=>r.kind==='checkpoint_arrival'&&r.corrects);
  const html=h(ArrivalRecord,{arrival:a,all:records});assert.match(html,/out\/new.md/);assert.doesNotMatch(html,/arrival is recorded as lapsed/);assert.match(html,/Post-end subject association not established/);
  const facets=outputStanding({name:'summary',form:'file',gating_checkpoint:a.body.checkpoint,promised_standing:['relied on by the person']},run({lifecycle:{records}}));assert.match(facets.humanActs,/^unknown:.*no established post-end subject association/);
  const {WorkflowRootPanel}=load('App.tsx');const full=h(WorkflowRootPanel,{data:dto,host:{state:'ready',generation:{},threads:[]},act:async()=>{}});assert.match(full,/Recorded post-end source history/);assert.ok(full.includes('act_lapsed'));assert.doesNotMatch(full,/arrival is recorded as lapsed/);
  for(const limited of [{...a,corrects:undefined,afterRunEndRelationLimit:'original counted source corrected'}, {...a,corrects:undefined}]) {
    const source=[...records.filter(r=>r.kind!=='checkpoint_arrival'),limited];if(!limited.afterRunEndRelationLimit)source.push({...limited,recordId:'duplicate-coordinate'});
    assert.doesNotMatch(h(ArrivalRecord,{arrival:limited,all:source}),/arrival is recorded as lapsed/);assert.match(outputStanding({name:'summary',gating_checkpoint:a.body.checkpoint},run({lifecycle:{records:source}})).humanActs,/^unknown:/);
  }
});

test('actual held lapse DTO qualifies its pending label and later write on the same observation',()=>{
  const {spawnSync}=createRequire(import.meta.url)('node:child_process');const {fileURLToPath}=createRequire(import.meta.url)('node:url');
  const proc=spawnSync('cargo',['+1.97.1','test','--offline','--locked','--lib','runtime_session::workflow_root_tests::after_end_file_lapse_pending_group_keeps_first_observation_through_later_edits','--','--exact','--nocapture','--test-threads=1'],{cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)),encoding:'utf8',env:{...process.env,CHIRALITY_SKIP_CODEX:'1'}});assert.equal(proc.status,0,proc.stderr+proc.stdout);
  const dto=marker=>{const line=proc.stdout.split('\n').find(line=>line.includes(marker));assert.ok(line);return JSON.parse(line.slice(line.indexOf(marker)+marker.length));};
  const pending=dto('AFTER_END_LAPSE_PENDING_DTO:');const records=pending.afterRunEnd.runs[0].records;const a=records.find(r=>r.kind==='checkpoint_arrival');const held=records.find(r=>r.kind==='act_lapsed');assert.equal(held.written,false);const html=h(ArrivalRecord,{arrival:a,all:records});assert.match(html,/arrival’s pending label is lapsed/);assert.match(html,/Not yet written to the run record/);assert.doesNotMatch(html,/arrival is recorded as lapsed/);
  const late=dto('AFTER_END_LAPSE_LATE_DTO:');const recovered=late.afterRunEnd.runs[0].records;assert.equal(recovered.filter(r=>r.recordId===held.recordId).length,1);const again=h(ArrivalRecord,{arrival:recovered.find(r=>r.kind==='checkpoint_arrival'),all:recovered});assert.match(again,/Written late; the run record carries/);assert.doesNotMatch(again,/pending label/);assert.equal(recovered.find(r=>r.recordId===held.recordId).observedAt,held.observedAt);
});
