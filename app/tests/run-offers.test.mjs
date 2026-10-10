import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';

const load=name=>{
  const url=new URL(`../src/${name}.tsx`,import.meta.url);
  const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX}});
  const exports={};new Function('require','exports',compiled.outputText)(createRequire(url),exports);return exports;
};
const {RunOffer}=load('RunOffers');
const {NativeActivityView}=load('NativeActivity');

// Offers in the host shape (WorkflowRootSession::offers in runtime_session.rs).
const message={threadId:'T',turnId:'t2',itemId:'m'};
const workflow={kind:'workflow',origin:'project',source_root:'/lib',name:'load-check',revision:'abcdef0123456789',revision_method:'m'};
const finished={message:'unused',run:'run:workflow:a',statement:'Workflow finished: project:supports-adjust',standing:"the agent's statement in its message; the person ended the run"};
const proposal=(extra={})=>({proposed:'project:load-check',resolution:{workflow,standing:'registered — selectable in this App session',notice:null},runInForce:null,standing:'x',...extra});
const g={appSession:'s',home:'h',spawnCounter:1};
const html=(offer,ready=true)=>renderToStaticMarkup(React.createElement(RunOffer,{offer,generation:g,ready,busy:false,act:async()=>{}}));
// Find the buttons of a rendered element tree (RunOffer holds no state, so it can be called directly).
const buttons=(node,found=[])=>{
  if(Array.isArray(node)){for(const n of node)buttons(n,found);return found;}
  if(!node||typeof node!=='object')return found;
  if(node.type==='button')found.push(node);
  buttons(node.props?.children,found);return found;
};
const pressAll=offer=>{const calls=[];const tree=RunOffer({offer,generation:g,ready:true,busy:false,act:async(command,args)=>{calls.push([command,args]);}});
  for(const b of buttons(tree))b.props.onClick();return calls;};

test('a finished report is the agent statement and ends nothing until the person presses End run (RN-7, FN-3)',()=>{
  const offer={message,finished,proposal:null};
  const h=html(offer);
  assert.match(h,/The agent wrote <q>Workflow finished: project:supports-adjust<\/q>\. This is the agent’s statement; run run:workflow:a stays in force until you end it\./);
  assert.match(h,/<button>End run<\/button>/);
  assert.match(h,/does not check or take the work as done/);
  assert.deepEqual(pressAll(offer),[['workflow_end_run',{runRef:'run:workflow:a',finishedReport:message}]],'the press names the message; the host re-reads it');
});

test('a proposal is never a start: the person starts it, and only one way at a time (RN-3, RN-4, PR-4)',()=>{
  const plain={message,finished:null,proposal:proposal()};
  const h=html(plain);
  assert.match(h,/The agent proposed <q>Next workflow: project:load-check<\/q>\. Nothing is selected or started unless you choose it\./);
  assert.match(h,/<button>Start load-check \(proposed by the agent\)<\/button>/);
  assert.ok(!/End .* and start/.test(h));
  assert.deepEqual(pressAll(plain),[['workflow_start_proposed',{generation:g,message,runRef:null,personText:''}]]);
  assert.match(html(plain,false),/<button disabled="">Start load-check/,'no start while Codex is not ready');
  const during={message,finished,proposal:proposal({runInForce:{run:'run:workflow:a',workflow:'supports-adjust',endCause:'completed'}})};
  const d=html(during);
  assert.ok(!/Start load-check \(proposed/.test(d),'no plain start while a run is in force');
  assert.match(d,/<button>End supports-adjust and start load-check<\/button>/);
  assert.match(d,/ends with cause “completed”/);assert.match(d,/<button>End run<\/button>/,'End run beside it');
  assert.deepEqual(pressAll(during),[['workflow_end_run',{runRef:'run:workflow:a',finishedReport:message}],['workflow_start_proposed',{generation:g,message,runRef:'run:workflow:a',personText:''}]]);
});

test('an unresolved proposal shows its notice and offers no start (RN-5, PR-3)',()=>{
  const offer={message,finished:null,proposal:proposal({resolution:{workflow:null,notice:'proposed workflow project:load-check is a draft only — not a workflow identity'}})};
  const h=html(offer);
  assert.match(h,/is a draft only — not a workflow identity/);assert.ok(!/<button/.test(h));
  assert.equal(html({message}),'','no offer, nothing shown');
});

test('the activity view places offers beneath their message and run markers at their turns (RN-1)',()=>{
  const row=(turnId,order,native)=>({threadId:'T',turnId,native,displayState:'completed',standing:'live-observed',observedOrder:order});
  const runText='[Chirality] Workflow run start: supports-adjust from the project library "/lib", revision abcdef012345, run run:workflow:a.\n<<<chirality-workflow supports-adjust@abcdef012345 begin>>>\nbody\n<<<chirality-workflow supports-adjust@abcdef012345 end>>>';
  const view={items:[row('t1',0,{id:'u',type:'userMessage',content:[{type:'text',text:runText},{type:'text',text:'My brief'}]}),row('t2',1,{id:'m',type:'agentMessage',text:'Done.\nWorkflow finished: project:supports-adjust'}),row('t3',2,{id:'z',type:'agentMessage',text:'Later'})],
    turns:[],turnRecords:[],revisions:[],descendants:[]};
  const run={reference:'run:workflow:a',conversation:'T',turn:'t1',endedAfterTurn:'t2',workflow:{name:'supports-adjust',revision:'abcdef0123456789'},lifecycle:{state:'ended by the person',end:{cause:'completed'}},finishedReport:{run:'run:workflow:a'}};
  const out=renderToStaticMarkup(React.createElement(NativeActivityView,{view,threadId:'T',runs:[run],offers:[{message,finished,proposal:null}],renderOffer:o=>React.createElement('span',null,`OFFER ${o.message.itemId}`)}));
  const start=out.indexOf('Workflow run started: <b>supports-adjust abcdef012345</b>');const brief=out.indexOf('My brief');
  const offer=out.indexOf('OFFER m');const end=out.indexOf('Run ended: <b>completed</b>');const later=out.indexOf('Later');
  assert.ok(start>=0&&start<brief&&brief<offer&&offer<end&&end<later,`order: ${[start,brief,offer,end,later]}`);
  assert.match(out,/<summary>Workflow run text the App supplied \(\d+ characters\)<\/summary>/,'the supplied bytes are folded and openable');
  assert.match(out,/you ended it on the agent&#x27;s “Workflow finished” statement/);
  const unrecorded=renderToStaticMarkup(React.createElement(NativeActivityView,{view,threadId:'T'}));
  assert.ok(!unrecorded.includes('Workflow run text the App supplied'),'text that only looks like run text is not folded without a recorded run start');
  const prepared={...run,lifecycle:{state:'prepared; not a run until its start turn is observed'},endedAfterTurn:null};
  assert.ok(!renderToStaticMarkup(React.createElement(NativeActivityView,{view,threadId:'T',runs:[prepared]})).includes('Workflow run started'),'a prepared run is not a run');
  const elsewhere={...run,turn:'gone',endedAfterTurn:null,lifecycle:{state:'open (live); only the person\'s explicit end ends it'}};
  assert.match(renderToStaticMarkup(React.createElement(NativeActivityView,{view,threadId:'T',runs:[elsewhere]})),/whose position this view cannot show/);
});
