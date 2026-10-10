import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const load=name=>{const url=new URL(`../src/${name}`,import.meta.url);const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});const exports={};new Function('require','exports',compiled.outputText)(createRequire(url),exports);return exports;};
const {RunPanel,DeclaredPart,SelectedWorkflow,CompatibilityAdvisory,outputStanding,StandingFacets,arrivalLabel,actLabel}=load('RunPanel.tsx');
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
  assert.ok(html.includes('no arrival recorded. This App does not yet record checkpoint arrivals'));
  assert.ok(html.includes('missing in record (no checkpoint_listed entry)'),'PD-7: what the record lacks is shown');
  assert.ok(html.includes('the act is recorded only when you perform it'));
  assert.ok(html.includes('present, currently unavailable: host reported unavailable'),'a runtime unavailability is a requirement outcome, not a hold');
  assert.ok(!FORBIDDEN.test(html),html.match(FORBIDDEN)?.[0]);
  assert.equal(arrivalLabel('waiting'),'reached; act not yet recorded');
  assert.equal(arrivalLabel('held'),'not a recorded disposition (held)');
  assert.deepEqual(['A4','A5','A6','A7','A12'].map(actLabel),['mark checked','accept','approve','rely','set grant']);
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
  assert.ok(app.includes('<SelectedWorkflow selection={data?.selection}/>')&&app.includes('<RunPanel run={run}/>'));
});
