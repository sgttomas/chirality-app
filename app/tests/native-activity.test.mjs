import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const url=new URL('../src/NativeActivity.tsx',import.meta.url);
const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});
const exports={};new Function('require','exports',compiled.outputText)(createRequire(url),exports);
const {NativeActivityView,activityModel,activityThreads,displayStateText,resultNotSupplied}=exports;

// Invented rows in the host snapshot shape (native_items.rs), native items per the pinned 0.160.0 ThreadItem.
const row=(turnId,observedOrder,native,extra={})=>({threadId:'T',turnId,native,displayState:'completed',standing:'live-observed',observationEnded:false,observedOrder,...extra});
const view=()=>({
  supplierStanding:'unverified-development',
  limits:['Tool success is not checking, acceptance or reliance.','Parent completion says nothing about children.'],
  items:[
    // Array order is the host's identity sort, deliberately unlike receipt order.
    row('turn-2',5,{id:'a-msg2',type:'agentMessage',text:'Second answer',phase:'final_answer'}),
    row('turn-1',2,{id:'c-cmd',type:'commandExecution',command:'ls -la',cwd:'/w',source:'unifiedExecStartup',status:'completed',exitCode:0,durationMs:12,aggregatedOutput:'file.txt',commandActions:[]},{startNative:{source:'agent'}}),
    row('turn-1',0,{id:'z-user',type:'userMessage',content:[{type:'text',text:'Please <b>list</b> files',text_elements:[]}]}),
    row('turn-1',1,{id:'y-reason',type:'reasoning',summary:['Thinking about listing'],content:[]}),
    row('turn-1',3,{id:'b-mcp',type:'mcpToolCall',server:'srv',tool:'read',arguments:{},status:'completed',result:null,error:null}),
    row('turn-1',4,{id:'d-file',type:'fileChange',status:'inProgress',changes:[{path:'a.txt',kind:{type:'update',move_path:null},diff:'+x'}]},{displayState:'not-completed',endReason:'turn ended without item completion'}),
    row('turn-2',6,{id:'e-cmd',type:'commandExecution',command:'rm x',cwd:'/w',status:'inProgress',commandActions:[]},{displayState:'waiting-on-request',requestRef:{requestIdentity:'r1'}}),
    row('turn-2',7,{id:'f-unknown',type:'futureTool',raw:42},{displayState:'unknown',observationEnded:true}),
    row('turn-2',8,{id:'turn-2-plan',type:'plan',text:'1. Do it'}),
    row('turn-2',9,{id:'g-spawn',type:'collabAgentToolCall',tool:'spawnAgent',status:'completed',senderThreadId:'T',receiverThreadIds:['C'],agentsStates:{C:{status:'running',message:null}},prompt:'help',model:null}),
    {threadId:'OTHER',turnId:'turn-x',native:{id:'o',type:'agentMessage',text:'Other thread text'},displayState:'completed',observedOrder:10},
    {threadId:'C',turnId:'child-turn',native:{id:'c1',type:'agentMessage',text:'Child says hi'},displayState:'in-progress',observedOrder:11},
  ],
  turns:[],
  turnRecords:[
    {threadId:'T',native:{id:'turn-2',status:'completed',startedAt:200,items:[]}},
    {threadId:'T',native:{id:'turn-1',status:'interrupted',startedAt:100,error:{message:'interrupted by request'},items:[]}},
  ],
  revisions:[
    {kind:'plan-item',revisionId:'pi',threadId:'T',turnId:'turn-2',itemId:'turn-2-plan',ordinal:1,typesPin:'0.160.0'},
    {kind:'checklist',revisionId:'cl1',threadId:'T',turnId:'turn-2',ordinal:1,content:{explanation:null,steps:[{step:'Read',status:'inProgress'}]}},
    {kind:'checklist',revisionId:'cl2',threadId:'T',turnId:'turn-2',ordinal:2,content:{explanation:'Updated',steps:[{step:'Read',status:'completed'},{step:'Write',status:'pending'}]}},
  ],
  descendants:[{threadId:'C',parentThreadId:'T',parentSource:'collabAgentToolCall.senderThreadId',statusSource:'collabAgentToolCall.agentsStates',lastObservedStatus:{status:'running'},guidance:'not-known',observationEnded:false}],
  goals:{T:{native:{objective:'Ship the slice'},source:'thread/goal/updated'}},
  checklistGaps:[{threadId:'T',turnId:'turn-0',reason:'checklist updates are not kept in Codex history; not recoverable after restart or relaunch'}],
});
const render=(v=view(),threadId='T')=>renderToStaticMarkup(React.createElement(NativeActivityView,{view:v,threadId}));

test('turns follow native start time and items follow receipt order, scoped to the thread',()=>{
  const model=activityModel(view(),'T');
  assert.deepEqual(model.turns.map(t=>t.turnId),['turn-1','turn-2']);
  assert.deepEqual(model.turns[0].items.map(r=>r.native.id),['z-user','y-reason','c-cmd','b-mcp','d-file']);
  assert.deepEqual(activityThreads(view()),['T','OTHER','C']);
  const late={items:[{threadId:'T',turnId:'late',native:{id:'x',type:'contextCompaction'},observedOrder:0},{threadId:'T',turnId:'early',native:{id:'y',type:'contextCompaction'},observedOrder:1},{threadId:'T',turnId:'unstarted',native:{id:'z',type:'contextCompaction'},observedOrder:2}],
    turnRecords:[{threadId:'T',native:{id:'late',status:'completed',startedAt:300}},{threadId:'T',native:{id:'early',status:'completed',startedAt:100}}]};
  assert.deepEqual(activityModel(late,'T').turns.map(t=>t.turnId),['early','late','unstarted'],'native start time outranks receipt order');
  const html=render();
  assert.ok(html.indexOf('Please')<html.indexOf('ls -la')&&html.indexOf('ls -la')<html.indexOf('Second answer'));
  assert.ok(!html.includes('Other thread text'));assert.ok(!html.includes('Child says hi'));
});

test('messages are readable, escaped and never presented as acts',()=>{
  const html=render();
  assert.ok(html.includes('Please &lt;b&gt;list&lt;/b&gt; files'));assert.ok(!html.includes('<b>list</b>'));
  assert.match(html,/User message<\/b> \(text Codex recorded as input; not an act\)/);
  assert.match(html,/Agent<\/b> · final answer/);assert.ok(html.includes('Thinking about listing'));
  assert.ok(html.includes('Goal (thread/goal/updated): Ship the slice'));
  assert.ok(html.includes('Turn error: interrupted by request'));
});

test('tool rows keep native status beside the display reading and invent no outcome',()=>{
  const html=render();
  assert.ok(html.includes('ls -la'));assert.ok(html.includes('exit code: 0'));assert.ok(html.includes('file.txt'));
  assert.ok(html.includes('agent at start, unifiedExecStartup at completion'));
  assert.match(html,/not completed \(turn ended\)<\/b> · native status inProgress/);
  assert.ok(html.includes('result not supplied by Codex'));
  assert.match(html,/waiting on a request<\/b>.*answer it on its request card/);
  assert.ok(!/<button/.test(html),'activity view offers no answer or act control');
  assert.match(html,/unknown — no completion observed<\/b> · native status <i>none in this item kind<\/i>/);
  assert.ok(html.includes('unfamiliar item <code>futureTool</code>'));assert.ok(html.includes('&quot;raw&quot;: 42'));
  assert.doesNotMatch(html.toLowerCase(),/\b(approved|accepted|verified|checked by|relied on|returned|integrated)\b/);
  assert.equal(displayStateText({displayState:'unknown'}),'unknown — no completion observed');
  assert.equal(resultNotSupplied({displayState:'not-completed',native:{type:'mcpToolCall',result:null,error:null}}),false);
});

test('plans, checklist revisions and their recovery gap are shown as observed',()=>{
  const html=render();
  assert.match(html,/Plan<\/b> · revision 1 in this conversation/);assert.ok(html.includes('1. Do it'));
  assert.ok(html.includes('revision 2 of 2 observed live'));assert.ok(html.includes('[completed] Read'));assert.ok(html.includes('[pending] Write'));
  assert.ok(html.includes('revision 1: [inProgress] Read'));
  assert.ok(html.includes('Checklist for turn turn-0: checklist updates are not kept in Codex history'));
  const v=view();v.items=v.items.map(r=>r.native.id==='turn-2-plan'?{...r,native:{id:r.native.id,type:'plan'},displayState:'in-progress',preview:'Draft plan',previewStanding:'in progress; may differ from completed plan'}:r);
  const draft=render(v);assert.ok(draft.includes('Draft plan'));assert.ok(draft.includes('may differ from completed plan'));
});

test('a completed parent turn says nothing about a running descendant',()=>{
  const html=render();
  assert.ok(html.includes('agent C: Codex status running'));
  assert.ok(html.includes('A completed turn here says nothing about these descendants.'));
  assert.ok(html.includes('C · last observed Codex status running'));
  assert.ok(html.includes('return, review and integration not inferred'));
  assert.ok(html.includes('guidance not known'));
  assert.ok(html.includes('<option value="C">descendant C</option>'));
});

test('empty and unselected states stay explicit',()=>{
  assert.ok(render(view(),null).includes('Select a conversation'));
  assert.ok(render({items:[],turns:[],revisions:[],descendants:[],goals:{},checklistGaps:[]},'T').includes('No activity observed'));
  assert.ok(render(null,'T').includes('No activity observed'));
});
