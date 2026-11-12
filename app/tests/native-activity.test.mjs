import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';
const url=new URL('../src/NativeActivity.tsx',import.meta.url);
const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX}});
const exports={};new Function('require','exports',compiled.outputText)(createRequire(url),exports);
const {NativeActivityView,RowBoundary,activityModel,displayStateText,resultNotSupplied}=exports;

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
  typesPin:'0.160.0',
  turns:[{id:'turn-2',status:'completed',startedAt:200,items:[]},{id:'turn-1',status:'interrupted',startedAt:100,error:{message:'interrupted by request'},items:[]}],
  turnRecords:[{threadId:'T',turnId:'turn-2'},{threadId:'T',turnId:'turn-1'}],
  revisions:[
    {kind:'plan-item',revisionId:'pi',threadId:'T',turnId:'turn-2',itemId:'turn-2-plan',ordinal:1,standing:'live-observed',typesPin:'0.160.0'},
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
  const item=(turnId,observedOrder)=>({threadId:'T',turnId,native:{id:turnId,type:'contextCompaction'},displayState:'completed',observedOrder});
  const late={items:[item('late',0),item('early',5),item('unstarted',2)],turns:[{id:'late',status:'completed',startedAt:300},{id:'early',status:'completed',startedAt:100}],turnRecords:[{threadId:'T',turnId:'late'},{threadId:'T',turnId:'early'}]};
  assert.deepEqual(activityModel(late,'T').turns.map(t=>t.turnId),['early','late','unstarted'],'native start time outranks receipt order; unstarted turns merge by receipt');
  const reversed={...late,items:[...late.items].reverse(),turns:[...late.turns].reverse(),turnRecords:[...late.turnRecords].reverse()};
  assert.deepEqual(activityModel(reversed,'T').turns.map(t=>t.turnId),['early','late','unstarted'],'input order does not matter');
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

test('native MCP and App tool result text is readable without fetching media and retains the complete result',()=>{
  const v=view();v.items=[
    row('turn-1',0,{id:'m',type:'mcpToolCall',server:'sample',tool:'read',status:'completed',result:{content:[{type:'text',text:'MCP <result>'},{type:'resource',resource:{uri:'invented://sample',text:'Resource result'}},{type:'image',data:'retained-native-data',mimeType:'image/png'}],structuredContent:{extra:'kept'}}}),
    row('turn-1',1,{id:'d',type:'dynamicToolCall',tool:'inspect',status:'completed',contentItems:[{type:'inputText',text:'App tool result'},{type:'inputImage',imageUrl:'https://example.invalid/never-fetch'}]}),
  ];
  const html=render(v);
  assert.ok(html.includes('result text:<pre')&&html.includes('MCP &lt;result&gt;')&&html.includes('Resource result')&&html.includes('App tool result'));
  assert.ok(html.includes('&quot;structuredContent&quot;')&&html.includes('retained-native-data')&&html.includes('never-fetch'));
  assert.doesNotMatch(html,/<img|<audio|<iframe|<a /);
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

test('the delegation view follows the host’s NPTD §7.1 reading, and arrived descendants are always shown',()=>{
  const empty={...view(),descendants:[]};
  const withReading=(v,delegation)=>renderToStaticMarkup(React.createElement(NativeActivityView,{view:v,threadId:'T',delegation}));
  const present={reading:'present',reason:null,readAt:'2026-10-10T00:00:00Z'};
  const missing={reading:'missing',reason:'the effective configuration sets features.multi_agent = false (NPTD §7.1 (2))',readAt:'2026-10-10T00:00:00Z'};
  const unread={reading:'not established',reason:'multiAgentVersion not read: no response (NPTD §7.1 (3))'};
  // Present: shown, empty or not.
  assert.match(withReading(empty,present),/Delegation available \(read 2026-10-10T00:00:00Z\); no descendants observed\./);
  assert.ok(withReading(view(),present).includes('<h4>Descendants</h4>'));
  // Missing: absent, with the first reason; descendants that arrive anyway are shown.
  const hidden=withReading(empty,missing);
  assert.match(hidden,/Delegation not available: the effective configuration sets features\.multi_agent = false \(NPTD §7\.1 \(2\)\)/);
  assert.doesNotMatch(hidden,/<h4>Descendants<\/h4>|no descendants observed/);
  const arrived=withReading(view(),missing);
  assert.ok(arrived.includes('<h4>Descendants</h4>')&&arrived.includes('Descendants that arrived anyway are shown below.'));
  // Not established: shown only when delegation items arrive.
  const quiet=withReading(empty,unread);
  assert.doesNotMatch(quiet,/Delegation availab|Delegation not available|<h4>Descendants/);
  const shown=withReading(view(),unread);
  assert.ok(shown.includes('<h4>Descendants</h4>')&&shown.includes('Delegation availability not established: multiAgentVersion not read'));
  assert.doesNotMatch(withReading(empty,undefined),/Delegation availab|Delegation not available|<h4>Descendants/,'no reading: nothing claimed');
});

test('empty and unselected states stay explicit',()=>{
  assert.ok(render(view(),null).includes('Select a conversation'));
  assert.ok(render({items:[],turns:[],revisions:[],descendants:[],goals:{},checklistGaps:[]},'T').includes('No activity observed'));
  assert.ok(render(null,'T').includes('No activity observed'));
});

test('an unfinished message, reasoning or compaction never reads as finished',()=>{
  for(const state of ['not-completed','unknown','in-progress']){
    const v=view();v.items=[row('turn-1',0,{id:'m',type:'agentMessage',text:'',phase:'final_answer'},{displayState:state,preview:'Partial ans',previewStanding:'streamed so far; may differ from the completed item'}),
      row('turn-1',1,{id:'r',type:'reasoning',summary:[],content:[]},{displayState:state,summaryPreview:['thinking part']}),
      row('turn-1',2,{id:'k',type:'contextCompaction'},{displayState:state})];
    const html=render(v);
    assert.equal((html.match(new RegExp(displayStateText({displayState:state}).replace(/[()]/g,'\\$&'),'g'))??[]).length,3,state);
    assert.ok(html.includes('Partial ans'));assert.ok(html.includes('streamed so far'));assert.ok(html.includes('thinking part'));
  }
  const done=view();done.items=[row('turn-1',0,{id:'m',type:'agentMessage',text:'Final',phase:'final_answer'},{preview:'stale'})];
  const html=render(done);assert.ok(html.includes('Final'));assert.ok(!html.includes('stale'));assert.ok(!html.includes('none in this item kind'),'a completed message shows no state line');
});

test('streamed plan and command previews show while in progress',()=>{
  const v=view();v.items=[row('turn-1',0,{id:'p',type:'plan',text:''},{displayState:'in-progress',preview:'1. Draft step',previewStanding:'in progress; may differ from completed plan'}),
    row('turn-1',1,{id:'c',type:'commandExecution',command:'make',cwd:'/w',status:'inProgress',commandActions:[]},{displayState:'in-progress',preview:'building...'})];
  const html=render(v);
  assert.ok(html.includes('1. Draft step'));assert.ok(html.includes('may differ from completed plan'));
  assert.ok(html.includes('output so far'));assert.ok(html.includes('building...'));
});

test('off-schema native values render as text instead of breaking the view',()=>{
  const v=view();v.items=[row('turn-1',0,{id:'w',type:'webSearch',query:{q:1}}),row('turn-1',1,{id:'c',type:'commandExecution',command:['ls'],cwd:'/w',status:{odd:true},commandActions:[]})];
  const html=render(v);
  assert.ok(html.includes('{&quot;q&quot;:1}'));assert.ok(html.includes('[&quot;ls&quot;]'));
});

test('every descendant in the subtree is selectable and roles show as Codex reports them',()=>{
  const v=view();v.descendants.push({threadId:'G',parentThreadId:'C',parentSource:'subAgentActivity containing thread (inference)',guidance:'not-known',nativeThread:{agentRole:'reviewer',agentNickname:null}});
  v.descendants[0].nativeThread={agentRole:'explorer',agentNickname:'Ada'};
  const html=render(v);
  assert.ok(html.includes('<option value="G">descendant G (of C)</option>'));
  assert.ok(html.includes('role explorer (as Codex reports)'));assert.ok(html.includes('nickname Ada'));
  assert.ok(html.includes('(status source collabAgentToolCall.agentsStates)'));
  const model=activityModel(v,'C');assert.equal(model.parent.parentThreadId,'T');
  assert.ok(!renderToStaticMarkup(React.createElement(NativeActivityView,{view:v,threadId:'C'})).includes('status source',html.indexOf('G ·')));
});

test('a plan read from Codex history shows no revision number',()=>{
  const v=view();v.revisions[0].standing='recovered-from-supplier';v.items=v.items.map(r=>r.native.id==='turn-2-plan'?{...r,standing:'recovered-from-supplier'}:r);
  const html=render(v);
  assert.match(html,/Plan<\/b><div>.*· read from Codex history/);assert.ok(!html.includes('in this conversation'));
  assert.equal(html.match(/read from Codex history/g).length,1,'the history label appears once');
  v.items=v.items.map(r=>r.native.id==='turn-2-plan'?{...r,standing:'live-observed'}:r);
  assert.match(render(v),/Plan<\/b> · revision read from Codex history/,'a recovered revision on a live row still says so');
  v.revisions[0].standing='something-else';assert.match(render(v),/Plan<\/b><div>/,'an unrecognised standing shows no ordinal');
});

test('off-schema collections and nested values render as text instead of throwing',()=>{
  const v=view();
  v.limits='one limit';
  v.items=[
    row('turn-1',0,{id:'r1',type:'reasoning',summary:'not an array',content:[]}),
    row('turn-1',1,{id:'r2',type:'reasoning',summary:{odd:1},content:[]}),
    row('turn-1',2,{id:'f1',type:'fileChange',status:'completed',changes:{path:'a'}}),
    row('turn-1',3,{id:'f2',type:'fileChange',status:'completed',changes:[null,{path:'b.txt',kind:{type:{deep:1}},diff:{d:2}}]}),
    row('turn-1',4,{id:'g1',type:'collabAgentToolCall',tool:{t:1},status:'completed',senderThreadId:'T',receiverThreadIds:'C',agentsStates:'running',prompt:{p:'obj prompt'}}),
    row('turn-1',5,{id:'g2',type:'collabAgentToolCall',tool:'spawnAgent',status:'completed',senderThreadId:'T',receiverThreadIds:[{id:'X'},'Y'],agentsStates:[]}),
    row('turn-1',6,{id:'c1',type:'commandExecution',command:'cat',cwd:'/w',status:'completed',exitCode:0,aggregatedOutput:{out:'obj output'},commandActions:[]}),
    row('turn-1',7,{id:'u1',type:'userMessage',content:[{type:'text',text:{t:'obj text'}}]}),
    row('turn-1',8,{id:'n1',type:{weird:true}}),
    row('turn-1',9,{id:'s1',type:'mcpToolCall',server:'s',tool:'t',status:{nested:'status'},result:{ok:1},error:null}),
  ];
  v.revisions=[{kind:'checklist',revisionId:'a',threadId:'T',turnId:'turn-1',ordinal:1,content:{steps:{not:'array'}}},
    {kind:'checklist',revisionId:{id:1},threadId:'T',turnId:'turn-1',ordinal:2,content:{steps:[null,{step:{s:1},status:{st:2}}]}}];
  v.descendants=[{threadId:'C',parentThreadId:'T',lastObservedStatus:{status:{deep:'status'}},guidance:'not-known'},
    {threadId:'D',parentThreadId:'T',lastObservedStatus:'running',guidance:'not-known'},
    {threadId:'E',parentThreadId:'T',lastObservedStatus:null,guidance:'not-known'}];
  const html=render(v);
  assert.ok(html.includes('one limit')===false,'a non-array limits value is not joined');
  assert.ok(html.includes('(none supplied)'));
  assert.ok(html.includes('b.txt'));assert.ok(html.includes('{&quot;deep&quot;:1}'));assert.ok(html.includes('{&quot;d&quot;:2}'));
  assert.ok(html.includes('{&quot;t&quot;:1}'));assert.ok(html.includes('to no receivers reported'));assert.ok(html.includes('obj prompt'));
  assert.ok(html.includes('to {&quot;id&quot;:&quot;X&quot;}, Y'));
  assert.ok(html.includes('obj output'));assert.ok(html.includes('{&quot;t&quot;:&quot;obj text&quot;}'));
  assert.ok(html.includes('unfamiliar item <code>{&quot;weird&quot;:true}</code>'));
  assert.ok(html.includes('native status {&quot;nested&quot;:&quot;status&quot;}'));
  assert.ok(html.includes('[{&quot;st&quot;:2}] {&quot;s&quot;:1}'));
  assert.ok(html.includes('C · last observed Codex status {&quot;deep&quot;:&quot;status&quot;}'));
  assert.ok(html.includes('D · last observed Codex status running'));assert.ok(html.includes('E · last observed Codex status not reported'));
  assert.ok(render({items:{},turns:'x',turnRecords:5,revisions:{},descendants:'d',checklistGaps:{}},'T').includes('No activity observed'));
  const latest=view();latest.revisions=[{kind:'checklist',revisionId:'l',threadId:'T',turnId:'turn-1',ordinal:1,content:{explanation:{e:1},steps:'not an array'}}];
  const latestHtml=render(latest);assert.ok(latestHtml.includes('revision 1 of 1'));assert.ok(latestHtml.includes('<ol></ol>'));assert.ok(latestHtml.includes('{&quot;e&quot;:1}'));
  for(const odd of ['__proto__','toString',{x:1}]) assert.equal(typeof displayStateText({displayState:odd}),'string');
});

test('a row that cannot be shown falls back to its raw native JSON and resets on a new row',()=>{
  // renderToStaticMarkup does not run error boundaries, so the boundary's own steps are exercised directly.
  const native={id:'x',type:'agentMessage',text:'raw <text>'},row={native};
  const boundary=new RowBoundary({value:native,row,label:'native item',children:React.createElement('span',null,'readable')});
  assert.equal(renderToStaticMarkup(boundary.render()),'<span>readable</span>');
  boundary.state={...boundary.state,...RowBoundary.getDerivedStateFromError(new Error('bad item'))};
  const fallback=renderToStaticMarkup(boundary.render());
  assert.ok(fallback.includes('This native item could not be shown readably'));assert.ok(fallback.includes('&quot;text&quot;: &quot;raw &lt;text&gt;&quot;'));
  assert.equal(RowBoundary.getDerivedStateFromProps({value:native,row},boundary.state),null,'the same row stays on its fallback');
  assert.deepEqual(RowBoundary.getDerivedStateFromProps({value:native,row:{native}},boundary.state),{failed:false,row:{native}},'a new row is tried again');
});

test('the host’s trial labels show on the trial turn and the linked sub-agent row (TT-2, TT-4)',()=>{
  const trialTurns=[{threadId:'T',turnId:'turn-2',label:'trial 4 of draft load-check; not a step of resolve-spacing’s run'},{threadId:'OTHER',turnId:'turn-1',label:'elsewhere'}];
  const trialChildren=[{threadId:'C',label:'sub-agent of trial 4 of draft load-check'}];
  const html=renderToStaticMarkup(React.createElement(NativeActivityView,{view:view(),threadId:'T',trialTurns,trialChildren}));
  const turn2=html.indexOf('Turn turn-2'),label=html.indexOf('trial 4 of draft load-check; not a step');
  assert.ok(label>turn2&&label<html.indexOf('Second answer'),'the label sits on turn-2’s row');
  assert.equal(html.match(/not a step of/g).length,1,'only the labelled turn');
  assert.ok(!html.includes('elsewhere'));
  assert.ok(html.includes('<b>sub-agent of trial 4 of draft load-check</b> · C · last observed'));
  assert.ok(!render().includes('trial 4'),'no labels without the host’s');
});

// Trial witness 2026-10-10 (c): conversation A (the parent) showed "Descendant of"
// its own child. A parent viewing its child is never labelled the child's descendant.
test('a parent viewing its child is not shown as a descendant of that child',()=>{
  const v={...view(),descendants:[
    {threadId:'C',parentThreadId:'T',parentSource:'subAgentActivity containing thread (inference)',guidance:'not-known',observationEnded:false},
    // The inverted inference an older host built from the child's own activity naming its parent.
    {threadId:'T',parentThreadId:'C',parentSource:'subAgentActivity containing thread (inference)',guidance:'not-known',observationEnded:false}]};
  const model=activityModel(v,'T');
  assert.equal(model.parent,null);
  assert.deepEqual(model.children.map(c=>c.threadId),['C']);
  const shown=renderToStaticMarkup(React.createElement(NativeActivityView,{view:v,threadId:'T'}));
  assert.doesNotMatch(shown,/Descendant of C/);
  assert.match(shown,/descendant C/,'the child stays listed under the parent');
  // The child itself still reads as the parent's descendant.
  assert.equal(activityModel({...v,descendants:[v.descendants[0]]},'C').parent.parentThreadId,'T');
});

// NPTD §5.7 (R19-2; PC-18): each plan revision and tool row is labelled with the run in force
// at its turn, from the App's run markers only; messages carry none; a row outside any run, or
// between runs, carries none; run B does not reset run A's plan revisions.
test('plan revisions and tool rows carry the run in force at their turn, from the run markers only',()=>{
  const turn=(id,startedAt)=>({id,status:'completed',startedAt,items:[]});
  const ids=['t1','t2','t3','t4','t5'];
  const v={supplierStanding:'unverified-development',limits:[],typesPin:'0.160.0',descendants:[],goals:{},checklistGaps:[],
    turns:ids.map((id,i)=>turn(id,100*(i+1))),turnRecords:ids.map(turnId=>({threadId:'T',turnId})),
    items:[
      row('t1',0,{id:'cmd-before',type:'commandExecution',command:'echo before',cwd:'/w',source:'agent',status:'completed',commandActions:[]}),
      row('t2',1,{id:'msg-a',type:'agentMessage',text:'Working in A'}),
      row('t2',2,{id:'plan-a',type:'plan',text:'1. A step'}),
      row('t3',3,{id:'cmd-a',type:'commandExecution',command:'echo a',cwd:'/w',source:'agent',status:'completed',commandActions:[]}),
      row('t4',4,{id:'plan-b',type:'plan',text:'1. B step'}),
      row('t5',5,{id:'web-b',type:'webSearch',query:'search in B'}),
    ],
    revisions:[
      {kind:'plan-item',revisionId:'p1',threadId:'T',turnId:'t2',itemId:'plan-a',ordinal:1,standing:'live-observed'},
      {kind:'plan-item',revisionId:'p2',threadId:'T',turnId:'t4',itemId:'plan-b',ordinal:2,standing:'live-observed'},
      {kind:'checklist',revisionId:'c1',threadId:'T',turnId:'t3',ordinal:1,content:{explanation:null,steps:[{step:'A-check',status:'completed'}]}},
    ]};
  const run=(reference,name,turnId,endedAfterTurn)=>({reference,conversation:'T',turn:turnId,workflow:{name,revision:`${name.toLowerCase()}0123456789abcdef`},
    lifecycle:endedAfterTurn?{state:'ended by the person',end:{cause:'ended by the person'}}:{state:'open (live)'},...(endedAfterTurn?{endedAfterTurn}:{})});
  const shown=runs=>renderToStaticMarkup(React.createElement(NativeActivityView,{view:v,threadId:'T',runs}));
  // The label within one row: from its text to the next row or checklist.
  const labelIn=(html,needle)=>{const i=html.indexOf(needle);assert.ok(i>=0,needle);
    const ends=[html.indexOf('id="item-',i),html.indexOf('<b>Checklist</b>',i)].filter(n=>n>=0);
    const m=html.slice(i,ends.length?Math.min(...ends):undefined).match(/During the run of <b>([^<]*)<\/b>/);return m?m[1]:null;};
  // Chained A→B: A from t2, ended after t3; B from t4, open.
  const chained=shown([run('run:a','WF-A','t2','t3'),run('run:b','WF-B','t4')]);
  assert.equal(labelIn(chained,'echo before'),null,'a row before any run carries no label');
  assert.equal(labelIn(chained,'Working in A'),null,'a message carries none');
  assert.equal(labelIn(chained,'1. A step'),'WF-A wf-a01234567');
  assert.equal(labelIn(chained,'echo a'),'WF-A wf-a01234567','a tool row inside run A, at its recorded end turn');
  assert.equal(labelIn(chained,'1. B step'),'WF-B wf-b01234567');
  assert.equal(labelIn(chained,'search in B'),'WF-B wf-b01234567','an open run stays in force');
  assert.match(chained,/Plan<\/b> · revision 1 in this conversation/);
  assert.match(chained,/Plan<\/b> · revision 2 in this conversation/,'run B does not reset run A’s plan (PC-18)');
  assert.equal(labelIn(chained,'A-check'),'WF-A wf-a01234567','a checklist revision carries its turn’s run');
  // A ended after t2, B from t4: t3 is between runs and carries none.
  const gap=shown([run('run:a','WF-A','t2','t2'),run('run:b','WF-B','t4')]);
  assert.equal(labelIn(gap,'echo a'),null,'a row between runs carries no label');
  assert.equal(labelIn(gap,'A-check'),null);
  assert.equal(labelIn(gap,'1. A step'),'WF-A wf-a01234567');
  // No runs: no labels; a run whose end turn is not shown is in force only at its start turn.
  assert.ok(!shown([]).includes('During the run of'));
  const unplaced=shown([run('run:a','WF-A','t2','t-missing')]);
  assert.equal(labelIn(unplaced,'1. A step'),'WF-A wf-a01234567');assert.equal(labelIn(unplaced,'echo a'),null);
  // A turn the view does not show is in no run.
  assert.equal(exports.runInForce([run('run:a','WF-A','t2')],['t1','t2'],'t9'),null);
});


test('messages and observed statuses stay readable while command and reasoning diagnostics are folded',()=>{
 const html=render();assert.match(html,/<section[^>]*aria-label="Conversation turn 1"/);
 assert.match(html,/<h4>Turn 1.*interrupted/);
 assert.match(html,/<details><summary>Command details<\/summary><code>ls -la<\/code>/);
 assert.match(html,/<details><summary>Command output<\/summary>/);
 assert.match(html,/<details><summary>Reasoning summary/);
 assert.match(html,/file.txt/);assert.match(html,/Second answer/);assert.doesNotMatch(html,/<details open/);
});


test('a nonzero command exit stays visible outside the optional command details',()=>{
 const v=view();v.items.find(r=>r.native.id==='c-cmd').native.exitCode=7;
 const html=render(v);assert.match(html,/<p role="status">Command exited with code 7\.<\/p><details><summary>Command details/);
});

// The case observed against an unreachable model: a live turn whose only news is Codex's repeated retry notice.
const notice=(turnId,receiptPosition,ordinalInTurn,extra={})=>({threadId:'T',turnId,error:{message:'Reconnecting... waiting for network',additionalDetails:'Connection failed: error sending request',codexErrorInfo:{responseStreamDisconnected:{httpStatusCode:null}}},willRetry:true,receiptPosition,ordinalInTurn,laterFrameForTurn:false,standing:'live-observed',...extra});
test('a turn’s error notices show in Codex’s words with the retry state it gave',()=>{
 const v=view();v.turns.push({id:'turn-3',status:'inProgress',startedAt:300,items:[]});v.turnRecords.push({threadId:'T',turnId:'turn-3'});
 v.turnErrors=[notice('turn-3',40,1),notice('turn-3',41,2),{...notice('turn-x',42,1),threadId:'OTHER'}];
 const html=render(v);
 assert.match(html,/<h4>Turn 3 · inProgress<\/h4>/);
 assert.match(html,/<div role="status" aria-label="Errors Codex reported in this turn"><p>Codex reported an error in this turn 2 times; the latest: <q>Reconnecting\.\.\. waiting for network — Connection failed: error sending request<\/q> Codex said it will retry\. No later event naming this turn has reached the App\.<\/p>/);
 assert.match(html,/The 2 error notices in the order received, each with its whole error object/);
 assert.match(html,/<li value="2">Reconnecting\.\.\. waiting for network — Connection failed: error sending request · will retry<small> · received at position 41<\/small><pre[^>]*>\{\n  &quot;message&quot;: &quot;Reconnecting\.\.\. waiting for network&quot;,\n  &quot;additionalDetails&quot;: &quot;Connection failed: error sending request&quot;,\n  &quot;codexErrorInfo&quot;: \{\n    &quot;responseStreamDisconnected&quot;: \{\n      &quot;httpStatusCode&quot;: null\n    \}\n  \}\n\}<\/pre><\/li>/);
 assert.equal(html.match(/Errors Codex reported in this turn/g).length,1,'another conversation’s notice is not shown here');
 // Later activity for the turn is said as received, never as a recovery.
 v.turnErrors=[notice('turn-3',40,1,{laterFrameForTurn:true})];
 const later=render(v);assert.match(later,/Codex reported an error in this turn: <q>.*<\/q> Codex said it will retry\. The App has since received a later event naming this turn\./);
 assert.doesNotMatch(later,/recovered|reconnected|resolved/i);
});
test('a final error notice alerts, and a stopped Codex or a dropped notice is said plainly',()=>{
 const v=view();v.turns.push({id:'turn-3',status:'inProgress',startedAt:300,items:[]});v.turnRecords.push({threadId:'T',turnId:'turn-3'});
 v.turnErrors=[notice('turn-3',70,34,{willRetry:false,error:{message:'stream disconnected before completion',codexErrorInfo:'other'}})];
 const html=render(v);
 assert.match(html,/<div role="alert" aria-label="Errors Codex reported in this turn"><p>Codex reported an error in this turn 34 times; the latest: <q>stream disconnected before completion<\/q> Codex said it will not retry\./);
 assert.match(html,/33 earlier notices are no longer kept\./);assert.match(html,/&quot;codexErrorInfo&quot;: &quot;other&quot;/);
 v.turnErrors=[notice('turn-3',40,1,{observationEnded:true})];
 assert.match(render(v),/The App stopped receiving from that Codex process before any later event naming this turn\./);
 assert.doesNotMatch(render(v),/Codex has stopped/,'the end of the App’s observation is not a claim about Codex’s process');
 // Error, then the turn's end, then the close: what arrived before the close is still what arrived.
 v.turns.find(t=>t.id==='turn-3').status='completed';
 v.turnErrors=[notice('turn-3',40,1,{observationEnded:true,laterFrameForTurn:true})];v.observationEnded=true;
 const ended=render(v);
 assert.match(ended,/The App has since received a later event naming this turn\./);assert.doesNotMatch(ended,/stopped receiving|No later event/);
 assert.match(ended,/<h4>Turn 3 · completed<\/h4>/);
 v.turns.find(t=>t.id==='turn-3').status='inProgress';v.observationEnded=false;
 // A notice for a turn the view has nothing else for still shows, under a turn of unknown status.
 v.turnErrors=[notice('turn-9',90,1,{willRetry:undefined})];
 const orphan=render(v);assert.match(orphan,/status unknown<\/h4>/);assert.match(orphan,/Codex did not say whether it will retry\./);
 assert.deepEqual(activityModel(v,'T').turns.at(-1).errors.length,1);
});

test('a turn last seen in progress is not headed in progress once Codex has stopped',()=>{
 const v=view();v.turns.push({id:'turn-3',status:'inProgress',startedAt:300,items:[]});v.turnRecords.push({threadId:'T',turnId:'turn-3'});
 assert.match(render(v),/<h4>Turn 3 · inProgress<\/h4>/);
 v.observationEnded=true;
 const html=render(v);
 assert.match(html,/<h4>Turn 3 · in progress when last observed; the App is no longer receiving from that Codex process, so its outcome is unknown<\/h4>/);
 assert.doesNotMatch(html,/<h4>Turn 3 · inProgress<\/h4>/);
 assert.match(html,/<h4>Turn 1 · interrupted<\/h4>/,'an observed end stays as observed');assert.match(html,/<h4>Turn 2 · completed<\/h4>/);
});

test('a frame named error that the App could not read is said as that and given no retry meaning',()=>{
 const v=view();v.turns.push({id:'turn-3',status:'inProgress',startedAt:300,items:[]});v.turnRecords.push({threadId:'T',turnId:'turn-3'});
 const unreadable=(turnId,receiptPosition,extra={})=>({threadId:'T',turnId,receiptPosition,observedOrder:receiptPosition,ordinalInTurn:1,kind:'not-the-pinned-error-notification',reason:'its meaning and retry state are not established',standing:'live-observed',...extra});
 v.unreadableTurnErrors=[unreadable('turn-3',50),unreadable('turn-x',51,{threadId:'OTHER'})];
 const only=render(v);
 assert.match(only,/<div aria-label="Frames named error that the App could not read"><p role="status">Codex sent a frame named <code>error<\/code> for this turn that the App could not read as the error notice its Codex version defines, so its meaning and retry state are not established\. Received at position 50; the original envelope is under Host diagnostics only while the host(&#x27;|')s journal still holds it\.<\/p><\/div>/);
 assert.doesNotMatch(only,/will retry|will not retry|Codex reported an error in this turn|kept unchanged|an error notice for this turn/);
 // A request from Codex that happened to be named error is said to be a request, not a notice.
 v.unreadableTurnErrors=[unreadable('turn-3',50,{kind:'server-request-named-error'})];
 const request=render(v);assert.match(request,/not established\. It was a request from Codex and not a notice\. Received at position 50;/);
 assert.doesNotMatch(request,/Errors Codex reported in this turn/,'a request that was not a notice is not labelled an error Codex reported');
 v.unreadableTurnErrors=[unreadable('turn-3',50,{kind:'server-request-named-error'}),unreadable('turn-3',51,{ordinalInTurn:2,kind:'server-request-named-error'})];
 assert.match(render(v),/not established\. They were requests from Codex and not notices\. Received at position 50, 51;/);
 // Beside a readable notice, and past the per-turn cap: the count is what was received, and what was kept is said.
 v.turnErrors=[notice('turn-3',40,1,{laterFrameForTurn:true})];
 v.unreadableTurnErrors=[unreadable('turn-3',60,{ordinalInTurn:11}),unreadable('turn-3',61,{ordinalInTurn:12,kind:'server-request-named-error'})];
 const both=render(v);
 assert.match(both,/Codex said it will retry\. The App has since received a later event naming this turn\./);
 assert.match(both,/Codex sent 12 frames named <code>error<\/code> for this turn that the App could not read.*their meaning and retry state are not established\. 1 of those kept was a request from Codex and not a notice\. The App kept the latest 2\. Received at position 60, 61; the original envelopes are under Host diagnostics only while the host(&#x27;|')s journal still holds them\./);
});

test('a turn known only by an error notice keeps its place in the receiving order',()=>{
 const v={items:[{threadId:'T',turnId:'later',native:{id:'m',type:'agentMessage',text:'x'},displayState:'completed',observedOrder:10}],turns:[],turnRecords:[],revisions:[],descendants:[],
  turnErrors:[{threadId:'T',turnId:'earlier',error:{message:'m'},willRetry:true,receiptPosition:2,ordinalInTurn:1,observedOrder:2,turnFirstObservedOrder:2,laterFrameForTurn:false}],
  unreadableTurnErrors:[{threadId:'T',turnId:'earliest',receiptPosition:1,observedOrder:1,turnFirstObservedOrder:1}]};
 assert.deepEqual(activityModel(v,'T').turns.map(t=>t.turnId),['earliest','earlier','later']);
 // The host keeps only a turn's newest notices: every notice kept for the earlier turn arrived after the later
 // turn's item, and the turn still stands where its first notice was received.
 v.turnErrors=[40,41].map((observedOrder,n)=>({threadId:'T',turnId:'earlier',error:{message:'m'},willRetry:true,receiptPosition:observedOrder,ordinalInTurn:33+n,observedOrder,turnFirstObservedOrder:2,laterFrameForTurn:false}));
 assert.deepEqual(activityModel(v,'T').turns.map(t=>t.turnId),['earliest','earlier','later']);
 // Without the first-order field (an older host), the kept notices' own order is all there is.
 v.turnErrors.forEach(e=>delete e.turnFirstObservedOrder);
 assert.deepEqual(activityModel(v,'T').turns.map(t=>t.turnId),['earliest','later','earlier']);
});

// The conversation-state notice, the selector suffix and the interrupted-turn note (LiveWorkNotice.tsx).
// Invented rows in the host status shape (hosting.rs threads, conversationTurns, serverRequests; interrupted_work.rs).
const LW=loadSrc('LiveWorkNotice');
const G={appSession:'s2',home:'app-home:aaaa',spawnCounter:1};
const lthread=(threadId,extra={})=>({generation:G,threadId,model:'m',...extra});
const applied=status=>({status,statusSource:{method:'thread/status/changed',receiptPosition:9}});
const lhost=(threads,extra={})=>({state:'ready',generation:G,threads,...extra});
const renderNotice=h=>renderToStaticMarkup(React.createElement(LW.LiveWorkNotice,{host:h,showConversation(){},findInHistory(){}}));
const asks=(threadId,extra={})=>({generation:G,state:'outstanding',classification:'known-answerable',originClass:'codex',nativeParameters:{threadId},...extra});

test('a conversation reads working, waiting or in error only from what Codex and the host report',()=>{
 const rows=[lthread('idle',applied({type:'idle'})),lthread('active',applied({type:'active',activeFlags:[]})),lthread('flag',applied({type:'active',activeFlags:['waitingOnApproval']})),
  lthread('error',applied({type:'systemError'})),lthread('admitted',{status:{type:'idle'}}),lthread('turn',{status:{type:'idle'}}),lthread('request',applied({type:'idle'})),
  lthread('service',applied({type:'idle'})),lthread('foreign',applied({type:'idle'})),lthread('unknown',{...applied(null)})];
 const h=lhost(rows,{conversationTurns:[{generation:G,threadId:'turn',nativeTurn:{status:'inProgress'}},{generation:G,threadId:'idle',nativeTurn:{status:'inProgress'},terminalEventObserved:false}],
  serverRequests:[asks('request'),asks('service',{originClass:'named-service'}),asks('foreign',{generation:{...G,spawnCounter:2}}),asks('idle',{classification:'unknown'})]});
 const words=id=>LW.conversationStateWords(h,rows.find(r=>r.threadId===id));
 assert.equal(words('idle'),'','Codex’s own idle report stands over a turn row the host has not seen end, and a request the person cannot answer is not waiting for them');
 assert.equal(words('active'),'working');assert.equal(words('error'),'Codex reported a system error');
 assert.equal(words('flag'),'Codex reports it is waiting for an approval or an answer','a waiting flag with no request is Codex’s report, as in the Run guide');
 assert.equal(words('admitted'),'');assert.equal(words('turn'),'working','before any status report, a turn seen starting and not ending');
 assert.equal(words('request'),'waiting for your answer','only a request the person can answer');
 assert.equal(words('service'),'','an outstanding named-service call is not the person’s to answer');
 assert.equal(words('foreign'),'','a request of another generation');
 assert.equal(words('unknown'),'','a status of unknown shape says nothing');
});

test('a stopped or replaced Codex establishes no state',()=>{
 const live=lthread('t',applied({type:'active',activeFlags:[]}));
 assert.equal(LW.conversationStateWords(lhost([live]),live),'working');
 assert.equal(LW.conversationStateWords(lhost([live],{generationClosed:true}),live),'');
 assert.equal(LW.conversationStateWords(lhost([live],{state:'exited-unexpectedly'}),live),'');
 assert.equal(LW.conversationStateWords(lhost([live],{generation:{...G,spawnCounter:2}}),live),'','a row of an earlier generation');
 const ended=lthread('t',{status:null,lastObservedStatus:{type:'active',activeFlags:[]},statusObservationEnded:true,statusSource:{method:'thread/status/changed',receiptPosition:9}});
 assert.equal(LW.conversationStateWords(lhost([ended]),ended),'','the last status seen is not a current reading');
 assert.equal(renderNotice(lhost([ended])),'');assert.equal(renderNotice(null),'');assert.equal(renderNotice(lhost([lthread('quiet',applied({type:'idle'}))])),'');
});

test('each state renders as one complete sentence with a way to show the conversation',()=>{
 const html=renderNotice(lhost([lthread('a',applied({type:'active',activeFlags:[]})),lthread('b',applied({type:'idle'})),lthread('c',applied({type:'systemError'})),
  lthread('d',applied({type:'active',activeFlags:['waitingOnUserInput']})),lthread('e',applied({type:'idle'}))],{serverRequests:[asks('e')]}));
 assert.match(html,/<section aria-label="Work in progress and interrupted work" role="status">/);
 assert.match(html,/<li>Conversation 1 · m is working\. <button>Show it<\/button><\/li>/);
 assert.match(html,/<li>Codex reported a system error in Conversation 3 · m\. <button>Show it<\/button><\/li>/);
 assert.match(html,/<li>Codex reports Conversation 4 · m is waiting for an approval or an answer; the request appears in the conversation once the App has received it\. <button>Show it<\/button><\/li>/);
 assert.match(html,/<li>Conversation 5 · m is waiting for your answer\. <button>Show it<\/button><\/li>/);
 assert.equal(html.match(/<li>/g).length,4);
 assert.doesNotMatch(html,/ is Codex /);
});

// interruptedWork as interrupted_work.rs gives it for home H-acct over physical home app-home:aaaa.
const SRC={appSession:'s1',home:'app-home:aaaa',spawnCounter:1};
const entry=(threadId,current,extra={})=>({threadId,home:'H-acct',physicalHome:'app-home:aaaa',sourceGeneration:SRC,priorSession:'s1',priorSessionEnd:'ended-without-record',lastRecordedState:'turn-live',
 turns:[{turnId:'u',current,...(extra.earlier?{earlier:extra.earlier}:{})}],...extra.entry});
const work=(...conversations)=>({home:'H-acct',physicalHome:'app-home:aaaa',conversations});

test('after a relaunch the notice says what the App last recorded, how that session ended, and only what Codex’s history said',()=>{
 const h=lhost([lthread('open')],{interruptedWork:work(entry('gone',{reading:'read',codexStatus:'interrupted',attempt:1}),entry('open',{reading:'not-read',attempts:0},{entry:{priorSessionEnd:'quit-with-live-work',lastRecordedState:'observation-lost'}}))});
 const html=renderNotice(h);
 assert.match(html,/The last thing the App recorded for a conversation \(<code>gone<\/code>\) before the previous App session ended was a turn in progress\. No end of that App session was recorded\. <span>When the App read Codex&#x27;s history, it reported that turn as interrupted\. <\/span>Reading it back resumed nothing and resent nothing\. <button>Find it in History<\/button>/);
 assert.match(html,/The last thing the App recorded for <strong>Conversation 1 · m<\/strong> before the previous App session ended was a turn in progress\. The App recorded that you quit it, and that this record was made when it stopped Codex for the quit\. <span>The App has not read that turn back from Codex\. <\/span><button>Show it<\/button>/);
 assert.doesNotMatch(html,/is working|now reports|Nothing was resumed|had a turn in progress|without a normal quit/);
});

test('each recorded end of the earlier session, and a loss before it, is said as recorded and apart from the turn',()=>{
 const words=e=>renderNotice(lhost([],{interruptedWork:work(e)}));
 assert.match(words(entry('t',{reading:'not-read'})),/No end of that App session was recorded\./);
 assert.match(words(entry('t',{reading:'not-read'},{entry:{priorSessionEnd:'system-terminated'}})),/in progress\. The App recorded that the system ended it\. <span>/);
 assert.match(words(entry('t',{reading:'not-read'},{entry:{priorSessionEnd:'quit-with-live-work'}})),/The App recorded that you quit it, and that this record was made when it stopped Codex for the quit\./);
 const unknownEnd=words(entry('t',{reading:'not-read'},{entry:{priorSessionEnd:'clean'}}));
 assert.doesNotMatch(unknownEnd,/The App recorded|No end of/,'an end value the App does not name says nothing');
 assert.match(words(entry('t',{reading:'not-read'},{entry:{lastRecordedState:'observation-lost',lostBeforeSessionEnd:'supplier-exit'}})),/in progress\. That record was made when Codex ended unexpectedly, before the App session ended\. No end of that App session was recorded\./);
 assert.match(words(entry('t',{reading:'not-read'},{entry:{lostBeforeSessionEnd:'supplier-stop',priorSessionEnd:'system-terminated'}})),/That record was made when Codex was stopped, before the App session ended\. The App recorded that the system ended it\./);
});

test('the latest read is the current one; an earlier read stays an earlier read, and nothing unread becomes an outcome',()=>{
 const W=LW.interruptedTurnWords;
 assert.equal(W({current:{reading:'read',codexStatus:'completed'}}),'When the App read Codex\'s history, it reported that turn as completed.');
 assert.equal(W({current:{reading:'read',codexStatus:'inProgress'}}),'When the App read Codex\'s history, it listed that turn as in progress; whether it finished is unknown.');
 assert.equal(W({current:{reading:'not-in-history'}}),'When the App read Codex\'s history, that turn was not in it; what became of it is unknown.');
 assert.equal(W({current:{reading:'unavailable',reason:'Codex did not answer'}}),'The App could not read it back from Codex (Codex did not answer); what became of it is unknown.');
 assert.equal(W({current:{reading:'not-read',attempts:2}}),'The App has not read that turn back from Codex.');
 assert.equal(W({current:{reading:'turn-not-named'}}),'The App read the conversation back from Codex, but that read did not name this turn; what became of it is unknown.');
 // A later failed read after an earlier success.
 const later=W({current:{reading:'unavailable',attempt:2,reason:'no answer'},earlier:{reading:'read',codexStatus:'completed',attempt:1}});
 assert.equal(later,'The App could not read it back from Codex (no answer); what became of it is unknown. An earlier read of Codex\'s history reported that turn as completed.');
 assert.match(W({current:{reading:'not-read'},earlier:{reading:'not-in-history'}}),/An earlier read of Codex's history did not find that turn\.$/);
 for(const turn of [{current:{reading:'not-established'}},{current:{reading:'read'}},{current:{reading:'read',codexStatus:7}},{},null]) assert.equal(W(turn),'What became of it is not established.');
});

test('the read sentence is only about the read, and stays true after the conversation is continued',()=>{
 // The person has since continued the conversation: it is working now in this generation.
 const h=lhost([lthread('t',applied({type:'active',activeFlags:[]}))],{interruptedWork:work(entry('t',{reading:'read',codexStatus:'interrupted',attempt:1}))});
 const html=renderNotice(h);
 assert.match(html,/Conversation 1 · m is working\./);
 assert.match(html,/Reading it back resumed nothing and resent nothing\./);
 assert.doesNotMatch(html,/Nothing was resumed|resumed or resent/);
 assert.doesNotMatch(renderNotice(lhost([],{interruptedWork:work(entry('t',{reading:'not-read'}))})),/Reading it back/,'no read, no sentence about one');
});

test('two homes with equal conversation and turn ids: nothing of the other home is shown, joined or offered',()=>{
 const loaded=lthread('t',applied({type:'idle'}));
 const foreignPhysical=entry('t',{reading:'read',codexStatus:'completed'},{entry:{physicalHome:'app-home:bbbb'}});
 const foreignClass=entry('t',{reading:'read',codexStatus:'failed'},{entry:{home:'H-key'}});
 const h=lhost([loaded],{interruptedWork:work(foreignPhysical,foreignClass)});
 assert.equal(renderNotice(h),'','neither another physical home nor another App-owned home is this one');
 assert.equal(LW.interruptedTurnNote(h,G,'t','u'),null);
 // This home's own entry beside them: only it is shown, with this home's conversation.
 const own=entry('t',{reading:'unavailable',reason:'no answer'});
 const mixed=lhost([loaded],{interruptedWork:work(foreignPhysical,own,foreignClass)});
 const html=renderNotice(mixed);
 assert.equal(html.match(/The last thing the App recorded/g).length,1);
 assert.match(html,/<strong>Conversation 1 · m<\/strong>.*could not read it back from Codex \(no answer\).*<button>Show it<\/button>/s);
 assert.doesNotMatch(html,/completed|failed/);
 assert.match(LW.interruptedTurnNote(mixed,G,'t','u'),/could not read it back from Codex \(no answer\)/);
 // A loaded conversation of another physical home is not this entry's conversation.
 const elsewhere=lhost([{...loaded,generation:{...G,home:'app-home:bbbb'}}],{generation:{...G,home:'app-home:bbbb'},interruptedWork:work(own)});
 const apart=renderNotice(elsewhere);
 assert.match(apart,/a conversation \(<code>t<\/code>\)/);assert.match(apart,/<button>Find it in History<\/button>/);assert.doesNotMatch(apart,/Show it/);
 assert.equal(LW.interruptedTurnNote(elsewhere,{...G,home:'app-home:bbbb'},'t','u'),null);
 // A reading that names no home shows nothing as this home's.
 assert.equal(renderNotice(lhost([loaded],{interruptedWork:{conversations:[own]}})),'');
 assert.deepEqual(LW.interruptedEntries(lhost([],{interruptedWork:{home:'H-acct',conversations:[own]}})),[]);
});

test('the interrupted turn carries the note derived from the host’s recovery reading, end to end through the activity view',()=>{
 const T=(current,extra={})=>({threadId:'T',home:'H-acct',physicalHome:'app-home:aaaa',sourceGeneration:SRC,priorSession:'s1',priorSessionEnd:'ended-without-record',lastRecordedState:'observation-lost',lostBeforeSessionEnd:'supplier-exit',turns:[{turnId:'turn-1',current}],...extra});
 const h=lhost([],{interruptedWork:work(T({reading:'read',codexStatus:'interrupted',attempt:1}),{...T({reading:'read',codexStatus:'completed'}),physicalHome:'app-home:bbbb',turns:[{turnId:'turn-2',current:{reading:'read',codexStatus:'completed'}}]})});
 const shown=(host,generation)=>renderToStaticMarkup(React.createElement(NativeActivityView,{view:view(),threadId:'T',restartNoteFor:(thread,turn)=>LW.interruptedTurnNote(host,generation,thread,turn)}));
 const html=shown(h,G);
 assert.equal(html.match(/<p role="note"><small>The last thing the App recorded of this turn/g).length,1,'turn-2’s entry belongs to another physical home');
 assert.match(html,/<h4>Turn 1 · interrupted<\/h4>.*?<p role="note"><small>The last thing the App recorded of this turn before the previous App session ended was that it was in progress\. That record was made when Codex ended unexpectedly, before the App session ended\. No end of that App session was recorded\. When the App read Codex&#x27;s history, it reported that turn as interrupted\. Reading it back resumed nothing and resent nothing\.<\/small><\/p>/s);
 const unread=shown(lhost([],{interruptedWork:work(T({reading:'not-read',attempts:0}))}),G);
 assert.match(unread,/<p role="note"><small>[^<]*The App has not read that turn back from Codex\.<\/small><\/p>/);
 assert.doesNotMatch(unread,/Reading it back|reported that turn as/);
 assert.doesNotMatch(shown(h,{...G,home:'app-home:bbbb'}),/turn-1.*The last thing/s);
 assert.doesNotMatch(render(view()),/The last thing the App recorded/);
});
