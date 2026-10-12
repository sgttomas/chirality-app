import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
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
  const unread={reading:'not established',reason:'namespaceTools not read: no response (NPTD §7.1 (4))'};
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
  assert.ok(shown.includes('<h4>Descendants</h4>')&&shown.includes('Delegation availability not established: namespaceTools not read'));
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
