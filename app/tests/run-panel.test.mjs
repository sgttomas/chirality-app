import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {localRequire} from './support/load-src.mjs';
const load=name=>{const url=new URL(`../src/${name}`,import.meta.url);const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});const exports={};new Function('require','exports',compiled.outputText)(localRequire(createRequire(url)),exports);return exports;};
const {RunBringBackView,RunPanel,DeclaredPart,SelectedWorkflow,CompatibilityAdvisory,outputStanding,StandingFacets,arrivalLabel,actLabel,RecordWriteNotice}=load('RunPanel.tsx');
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

test('an arrival bound to an output is evidence of where it was put, never a standing',()=>{
  const output={name:'summary',promised_standing:[]};
  const bound=[entry('run_opened',{}),listedCheck,arrival('CP-sum',1,'item:thread/turn/m2','output summary: agentMessage m2'),disposition('CP-sum',1,'waiting')];
  const facets=outputStanding(output,run({lifecycle:{state:'open',records:bound}}));
  assert.equal(facets.evidence,'observed in the conversation only: item:thread/turn/m2 (arrival of CP-sum). That marks where the agent put the output; it does not show that its content meets the declaration');
  assert.equal(facets.humanActs,'none recorded in this run (acts on App files are in their own act log)');
  assert.equal(facets.hostChecks,'none reported');
  // Another output keeps "missing"; a disposition other than waiting, or an unreadable body, reads unknown.
  assert.ok(outputStanding({name:'examination-report'},run({lifecycle:{state:'open',records:bound}})).evidence.startsWith('missing'));
  const performed=outputStanding(output,run({lifecycle:{state:'open',records:[...bound,disposition('CP-sum',1,'performed')]}}));
  assert.ok(Object.values(performed).every(v=>v.startsWith('unknown')),JSON.stringify(performed));
  const bodiless=outputStanding(output,run({lifecycle:{state:'open',records:record(['run_opened','checkpoint_arrival'])}}));
  assert.ok(Object.values(bodiless).every(v=>v.startsWith('unknown')));
});

test('standing facets show only what the run record supports',()=>{
  const output={name:'resolution-report',promised_standing:['host checks passed: spacing']};
  const facets=outputStanding(output,run());
  assert.deepEqual(facets,{temporal:'unknown: no result for this output is recorded',hostChecks:'none reported',limitations:'none reported',
    humanActs:'none recorded in this run (acts on App files are in their own act log)',examination:'none recorded',
    evidence:'missing: no record of resolution-report in the run record',route:'not recorded'});
  // A record holding entries this view does not read makes the facets unknown, never stronger.
  const withActs=outputStanding(output,run({lifecycle:{state:'open',records:record(['run_opened','human_act','examination_findings'])}}));
  assert.ok(Object.values(withActs).every(v=>v.startsWith('unknown')),JSON.stringify(withActs));
  // Only kinds known to say nothing about outputs leave "none recorded"; any other kind, including future ones, reads unknown.
  for(const kind of ['act_counted','item_decision','continued_past','observation_lost','evidence_limit','operation_entry','a_kind_not_yet_defined']){
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

test('the selected workflow shows its declared part instead of a JSON dump',()=>{
  const html=h(SelectedWorkflow,{selection:{identity:{name:'resolve-spacing',origin:'project',revision:'0123456789abcdef'},standing:'registered',runnable:true,declaration:declaration()}});
  assert.ok(html.includes('Selected: <b>resolve-spacing</b> (project), revision 0123456789ab'));
  assert.ok(html.includes('<b>CP-accept</b>'));
  assert.ok(h(SelectedWorkflow,{selection:{state:'not-selected'}}).includes('No workflow selected.'));
  assert.ok(h(DeclaredPart,{declaration:{unavailable:'workflow text unreadable'}}).includes('Declared part could not be read: workflow text unreadable'));
  const undeclared=h(DeclaredPart,{declaration:{raw:null,reading:'undeclared',categories:Object.fromEntries(cats.map(c=>[c,'undeclared'])),elements:{},findings:[]}});
  assert.ok(undeclared.includes('declares no requirements part')&&undeclared.includes('Not declared.'));
  const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
  assert.ok(app.includes('<SelectedWorkflow selection={data?.selection}/>')&&app.includes('<RunPanel run={run} conversations={conversations} busy={busy} act={action}/>'));
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
