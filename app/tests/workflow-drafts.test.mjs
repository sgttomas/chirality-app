import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,readdirSync} from 'node:fs';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';

const {WorkflowDraftsView,WorkflowDraftsList,DraftRow,TrialRow,CompareResult,draftStateWords,attributionWords,fidelityWords,trialSide,runSide,initialDraftsState}=loadSrc('WorkflowDrafts');

// Drafts in the host shape (WorkflowRootSession::drafts_view over
// registration::drafts::observe_drafts in the Rust host).
const content={method:'chirality.app.workflow-package.sha256/v1',value:'0123456789abcdef0123'};
const key={draft_location:'project',draft_root:'/p/.chirality/workflow-drafts',name:'load-check'};
const draft=(extra={})=>({name:'load-check',state:'draft',content,fileCount:2,findings:[],base:null,
  baseLimit:'no App-recorded base: a draft the agent or person wrote (WR §3, U-WR-12)',attribution:{kind:'not observed'},
  reference:{draft:key},slot:{registeredRevisions:0,identicalTo:null},tryLimit:null,reviewLimit:null,trials:[],
  standing:'draft — not a registered workflow; no workflow identity (EXEC TR-1)',...extra});
const g={appSession:'s',home:'h',spawnCounter:1};
const conv=(threadId)=>({generation:g,threadId,model:'gpt-x',modelProvider:'openai'});
const conversations=[conv('auth'),conv('other')];
const ckey=c=>JSON.stringify([c.generation,c.threadId]);

// Walks an element tree, rendering hookless function components, and collects matching elements.
const find=(node,match,found=[])=>{
  if(Array.isArray(node)){for(const n of node)find(n,match,found);return found;}
  if(!node||typeof node!=='object')return found;
  if(typeof node.type==='function')return find(node.type(node.props),match,found);
  if(match(node))found.push(node);
  find(node.props?.children,match,found);return found;
};
const label=node=>renderToStaticMarkup(node);
const button=(tree,name)=>{const b=find(tree,n=>n.type==='button'&&label(n).includes(name));assert.equal(b.length>0,true,`button ${name}`);return b[0];};
const spy=()=>{const calls=[];const act=async(c,a)=>{calls.push([c,a]);return {ok:true};};return {calls,act};};
const row=(d,props={})=>{const s=spy();const tree=DraftRow({draft:d,authoring:null,conversations,busy:false,act:s.act,...props});return {tree,calls:s.calls};};
const html=(d,props={})=>renderToStaticMarkup(React.createElement(DraftRow,{draft:d,authoring:null,conversations,busy:false,act:async()=>{},...props}));

test('each WR §5.1 state reads in the NIR §7 words, never as acceptance or checking',()=>{
  assert.equal(draftStateWords('draft'),'draft — not registered');
  assert.equal(draftStateWords('not valid'),'draft — not valid for registration');
  assert.equal(draftStateWords('changed since review'),'changed since review — review again before registering');
  assert.match(draftStateWords('under review',content),/under review \(reviewed content 0123456789ab\)/);
  assert.match(draftStateWords('registered, unchanged since'),/^registered, unchanged since/);
  assert.match(draftStateWords('future-state'),/reported as “future-state”/);
  for(const s of ['draft','not valid','under review','changed since review','registered, unchanged since'])
    assert.doesNotMatch(draftStateWords(s,content),/accept|approv|check(ed)?\b|reli|verified/i);
});

test('attribution reads "not observed" unless the host observed a file change item or an App action (D-3)',()=>{
  assert.equal(attributionWords({kind:'not observed'}),'not observed');
  assert.equal(attributionWords(undefined),'not observed');
  assert.equal(attributionWords({kind:'guessed'}),'not observed');
  assert.match(attributionWords({kind:'file change item',thread:'T',item:'fc-1'}),/file-change item fc-1 \(conversation T\)/);
  assert.match(attributionWords({kind:'app action'}),/written by this App/);
  assert.match(html(draft()),/Attribution: not observed\./);
});

test('Try with the authoring agent prepares a delegated trial in the chosen authoring conversation and sends nothing else (TT-3a, TT-11)',()=>{
  const {tree,calls}=row(draft(),{authoring:conversations[0]});
  const b=button(tree,'Try with the authoring agent');
  assert.equal(b.props.disabled,false);
  b.props.onClick();
  assert.deepEqual(calls,[['workflow_trial_prepare',{name:'load-check',kind:'delegated',generation:g,threadId:'auth'}]]);
});

test('Try with the authoring agent is disabled without a chosen conversation, pointing to the fresh-conversation trial',()=>{
  const {tree}=row(draft());
  assert.equal(button(tree,'Try with the authoring agent').props.disabled,true);
  assert.match(html(draft()),/Choose an authoring conversation above to try with the authoring agent, or try in a fresh conversation/);
});

test('Try in a fresh conversation is optional and prepares a clean trial, with or without an authoring conversation (TT-3b)',()=>{
  const none=row(draft());
  const b=button(none.tree,'Try in a fresh conversation');
  assert.equal(b.props.disabled,false);
  b.props.onClick();
  assert.deepEqual(none.calls,[['workflow_trial_prepare',{name:'load-check',kind:'clean',generation:null,threadId:null}]]);
  const chosen=row(draft(),{authoring:conversations[1]});
  button(chosen.tree,'Try in a fresh conversation').props.onClick();
  assert.deepEqual(chosen.calls,[['workflow_trial_prepare',{name:'load-check',kind:'clean',generation:g,threadId:'other'}]]);
  const h=html(draft());
  assert.match(h,/A trial is not a workflow run, registration, checking or acceptance/);
  assert.match(h,/The fresh-conversation trial is optional/);
  assert.match(h,/nothing is sent until you press Send/);
  assert.doesNotMatch(h,/attachment/i,'the attachment pre-fill is withdrawn');
});

test('both Try buttons are disabled with the host’s try limit shown',()=>{
  const limited=draft({tryLimit:'cannot be tried: content identity not established (HY-3)'});
  const {tree}=row(limited,{authoring:conversations[0]});
  assert.equal(button(tree,'Try with the authoring agent').props.disabled,true);
  assert.equal(button(tree,'Try in a fresh conversation').props.disabled,true);
  assert.match(html(limited,{authoring:conversations[0]}),/cannot be tried: content identity not established \(HY-3\)/);
});

test('no source file uses the withdrawn workflow_try_draft command',()=>{
  const dir=new URL('../src/',import.meta.url);
  for(const name of readdirSync(dir).filter(n=>/\.(tsx?|mjs|js)$/.test(n)))
    assert.doesNotMatch(readFileSync(new URL(name,dir),'utf8'),/workflow_try_draft/,name);
});

test('a draft is reviewed by its listed name and a refused draft shows its refusal',()=>{
  const r=row(draft());button(r.tree,'Review for registration').props.onClick();
  assert.deepEqual(r.calls,[['workflow_review_draft',{name:'load-check'}]]);
  const refused=draft({state:'not valid',findings:['HY-4: operating-system entry .DS_Store'],reviewLimit:'cannot be reviewed for registration (DS-5): HY-4: operating-system entry .DS_Store'});
  assert.equal(button(row(refused).tree,'Review for registration').props.disabled,true);
  const h=html(refused);
  assert.match(h,/HY-4: operating-system entry .DS_Store/);
  assert.match(h,/DS-5/);
  assert.match(h,/separate A15 act through the native confirmation/,'registration stays the person’s act');
});

// TT-4 trial rows in the host's listing shape.
const trial=(over={})=>({reference:'trial:1',sequence:3,kind:'delegated',content,version:'current',authoringConversation:{generation:g,threadId:'auth'},trialConversation:null,
  subAgent:{state:'sub-agent not linked'},fidelity:{state:'not checked',limits:[]},broughtBack:[],time:'2026-10-10T01:00:00Z',
  standing:'trial of a draft; not a run of any workflow identity; not registration, checking or acceptance',snapshot:{state:'current',reading:'trial snapshot unchanged'},
  live:false,filesOutsideWorkFolder:null,workFolder:'.chirality/workflow-trials/w1',...over});
const trialTree=(t,state=initialDraftsState)=>{const s=spy();const updates=[];const tree=TrialRow({trial:t,conversations,busy:false,act:s.act,state,update:p=>updates.push(p)});return {tree,calls:s.calls,updates};};
const trialHtml=(t,state=initialDraftsState)=>renderToStaticMarkup(React.createElement(TrialRow,{trial:t,conversations,busy:false,act:async()=>{},state,update:()=>{}}));

test('trial rows read each state in the design’s words (TT-4, TT-9)',()=>{
  assert.equal(fidelityWords({state:'verbatim',header_present:true}),'workflow given verbatim (trial header present)');
  assert.equal(fidelityWords({state:'differs',difference:'workflow body differs'}),"the sub-agent's input differs from the run text: workflow body differs");
  assert.equal(fidelityWords({state:'not checked'}),'not checked');
  assert.equal(fidelityWords(undefined),'not checked');
  const plain=trialHtml(trial());
  assert.match(plain,/Trial 3/);
  assert.match(plain,/delegated \(with the authoring agent\)/);
  assert.match(plain,/Content 0123456789ab \(current version\)/);
  assert.match(plain,/authoring conversation auth/);
  assert.match(plain,/sub-agent not linked/);
  assert.match(plain,/Fidelity: not checked/);
  assert.match(plain,/Snapshot: trial snapshot unchanged/);
  assert.match(plain,/Not brought back/);
  const rich=trialHtml(trial({version:'earlier',subAgent:{state:'linked',thread:'child-1',linkedBy:'automatically',alsoGiven:['child-2']},
    fidelity:{state:'differs',difference:'framing differs, workflow body equal',limits:['header not compared']},
    broughtBack:[{time:'2026-10-10T02:00:00Z',to:{generation:g,threadId:'auth'}}],filesOutsideWorkFolder:{count:2,reading:'files changed outside the trial work folder: 2 (from file-change items; shell writes not observed)'}}));
  assert.match(rich,/earlier version/);
  assert.match(rich,/sub-agent child-1 \(linked automatically\)/);
  assert.match(rich,/also given this trial&#x27;s workflow: child-2/);
  assert.match(rich,/the sub-agent&#x27;s input differs from the run text: framing differs, workflow body equal \(header not compared\)/);
  assert.match(rich,/Brought back: 2026-10-10T02:00:00Z to auth/);
  assert.match(rich,/files changed outside the trial work folder: 2/);
  const verbatim=trialHtml(trial({kind:'clean',subAgent:null,trialConversation:{generation:g,threadId:'clean-1'},fidelity:{state:'verbatim',header_present:false,limits:[]}}));
  assert.match(verbatim,/clean \(fresh conversation\)/);
  assert.match(verbatim,/trial conversation clean-1/);
  assert.match(verbatim,/workflow given verbatim \(trial header not present\)/);
  const earlier=trialHtml({kind:'earlier attachment trial',content,version:'changed since it was tried',conversation:'thread-a',time:'t0'});
  assert.match(earlier,/Earlier attachment trial · content 0123456789ab \(changed since it was tried\) · conversation thread-a · t0/);
});

test('trial row buttons call exactly their host commands (TT-9, TT-11)',()=>{
  const t=trial({subAgent:{state:'sub-agent not linked',unread:['child-9']}});
  let r=trialTree(t);
  button(r.tree,'Try again').props.onClick();
  button(r.tree,'Read again').props.onClick();
  button(r.tree,'Link as trial 3').props.onClick();
  assert.deepEqual(r.calls,[['workflow_trial_again',{reference:'trial:1'}],['workflow_trial_read',{reference:'trial:1'}],['workflow_trial_link',{reference:'trial:1',childThread:'child-9'}]]);
  r=trialTree(trial({subAgent:{state:'linked',thread:'child-1'}}));
  button(r.tree,'Unlink').props.onClick();
  assert.deepEqual(r.calls,[['workflow_trial_unlink',{reference:'trial:1',childThread:'child-1'}]]);
  assert.equal(find(trialTree(trial()).tree,n=>n.type==='button'&&/Link as|Unlink/.test(label(n))).length,0,'no link controls without children');
});

test('Bring trial back targets the authoring conversation by default, another the person picks, and waits while a turn is live (TT-10)',()=>{
  let r=trialTree(trial());
  const b=button(r.tree,'Bring trial back');
  assert.equal(b.props.disabled,false);
  b.props.onClick();
  assert.deepEqual(r.calls,[['workflow_trial_bring_back',{reference:'trial:1',generation:g,threadId:'auth',includeNative:false}]]);
  r=trialTree(trial(),{...initialDraftsState,bbTarget:{'trial:1':ckey(conversations[1])},bbNative:{'trial:1':true}});
  button(r.tree,'Bring trial back').props.onClick();
  assert.deepEqual(r.calls,[['workflow_trial_bring_back',{reference:'trial:1',generation:g,threadId:'other',includeNative:true}]]);
  const live=trialTree(trial({live:true}));
  assert.equal(button(live.tree,'Bring trial back').props.disabled,true);
  assert.match(trialHtml(trial({live:true})),/waits until no turn is live/);
  assert.equal(button(trialTree(trial({authoringConversation:null})).tree,'Bring trial back').props.disabled,true,'no target, no bring back');
  assert.deepEqual(trialTree(trial()).calls,[],'rendering a row calls nothing');
});

test('Compare calls workflow_trial_compare with the two chosen sides and shows the difference without judging (TT-11)',async()=>{
  const data={library:'l',observedAt:'t',drafts:[draft({trials:[trial()]})],transitions:[]};
  const s=spy();const updates=[];
  const state={...initialDraftsState,chosen:[trialSide('trial:1'),runSide('run-1')]};
  const tree=WorkflowDraftsList({data,workspace:true,conversations,runs:[{reference:'run-1'}],busy:false,act:s.act,state,update:p=>updates.push(p)});
  const compare=find(tree,n=>n.type==='button'&&/>Compare<\/button>$/.test(label(n)))[0];
  assert.ok(compare);
  assert.equal(compare.props.disabled,false);
  compare.props.onClick();
  assert.deepEqual(s.calls,[['workflow_trial_compare',{left:{trial:'trial:1'},right:{run:'run-1'}}]]);
  await new Promise(r=>setTimeout(r,0));
  assert.deepEqual(updates.at(-1),{compared:{ok:true}});
  const one=WorkflowDraftsList({data,workspace:true,conversations,runs:[{reference:'run-1'}],busy:false,act:s.act,state:{...initialDraftsState,chosen:[trialSide('trial:1')]},update:()=>{}});
  assert.equal(find(one,n=>n.type==='button'&&/>Compare<\/button>$/.test(label(n)))[0].props.disabled,true,'Compare needs exactly two sides');
  // Ticking a trial adds its side.
  const fresh=[];WorkflowDraftsList({data,workspace:true,conversations,busy:false,act:s.act,state:initialDraftsState,update:p=>fresh.push(p)});
  const box=find(TrialRow({trial:trial(),conversations,busy:false,act:s.act,state:initialDraftsState,update:p=>fresh.push(p)}),n=>n.type==='input'&&n.props.type==='checkbox')[0];
  box.props.onChange();
  assert.deepEqual(fresh.at(-1),{chosen:[trialSide('trial:1')]});
  const result={left:{label:'trial 3',kind:'delegated',version:'earlier',conversation:'child-1',snapshot:{reading:'unchanged'},summary:{turns:2,endings:['completed'],commands:{run:4,failed:1,list:['ls']},fileChanges:3,finalAgentMessage:'Done.',limits:[]}},
    right:{label:'run run-1',kind:'run',version:'registered abc',conversation:'auth',snapshot:{reading:'revision store'},summary:{turns:1,endings:['interrupted'],commands:{run:1,failed:0,list:[]},fileChanges:0,finalAgentMessage:'Stopped.',limits:['page 2 unreadable']}},
    difference:{files:[{path:'WORKFLOW.md',change:'modified',before:'aaaaaaaaaaaaaaaa',after:'bbbbbbbbbbbbbbbb',text:'- old step\n+ new step',lines:null,limit:null}],unchanged:2,standing:'per-file line difference'},standing:'side by side; not scored or judged'};
  const h=renderToStaticMarkup(React.createElement(CompareResult,{result}));
  assert.match(h,/trial 3/);assert.match(h,/run run-1/);
  assert.match(h,/Commands failed<\/th><td>1<\/td><td>0<\/td>/);
  assert.match(h,/WORKFLOW.md: modified \(aaaaaaaaaaaa → bbbbbbbbbbbb\)/);
  assert.match(h,/- old step\n\+ new step/);
  assert.match(h,/page 2 unreadable/);
  assert.match(h,/not scored or judged/);
  assert.doesNotMatch(h,/score:|better|worse|pass|fail(ed)? the/i);
  assert.match(renderToStaticMarkup(React.createElement(CompareResult,{result:{...result,difference:{limit:'version bytes not available'}}})),/version bytes not available/);
});

test('the list offers the project library, refresh, the authoring conversation choice and observed changes',()=>{
  const data={library:'workflow-library:1',observedAt:'2026-10-10T00:00:01Z',limit:null,standing:'observed by this App when listed',drafts:[draft(),draft({name:'site-visit'})],
    transitions:[{time:'t1',draft:{name:'load-check'},event:'written',from:'absent',to:'draft',attribution:{kind:'not observed'}}]};
  const h=renderToStaticMarkup(React.createElement(WorkflowDraftsView,{data,conversations,workspace:true,busy:false,act:async()=>{}}));
  assert.match(h,/Open this App project’s workflow library/);
  assert.match(h,/Refresh draft list/);
  assert.match(h,/Authoring conversation <select><option value="" selected="">None chosen<\/option>/,'defaults to none');
  assert.match(h,/aria-label="Draft load-check"/);
  assert.match(h,/aria-label="Draft site-visit"/);
  assert.match(h,/load-check: written \(absent → draft\); attribution not observed/);
  const none=renderToStaticMarkup(React.createElement(WorkflowDraftsView,{data:undefined,workspace:false,busy:false,act:async()=>{}}));
  assert.match(none,/No explicit App project is configured/);
  assert.match(none,/Open a library to list its drafts/);
  const empty=renderToStaticMarkup(React.createElement(WorkflowDraftsView,{data:{...data,drafts:[],transitions:[]},workspace:true,busy:false,act:async()=>{}}));
  assert.match(empty,/No drafts in this library/);
  // Choosing the authoring conversation is the person's; the delegated Try then uses it.
  const chosen=WorkflowDraftsList({data,conversations,workspace:true,busy:false,act:async()=>{},state:{...initialDraftsState,authoring:ckey(conversations[0])},update:()=>{}});
  assert.equal(button(chosen,'Try with the authoring agent').props.disabled,false);
});

test('damaged trial pointers and non-conforming transitions are shown, not hidden',()=>{
  const data={library:'l',observedAt:'t',drafts:[],transitions:[],transitionLimits:['draft x: changed transition not reported: WR draft_transition refused']};
  const h=renderToStaticMarkup(React.createElement(WorkflowDraftsView,{data,workspace:true,pointerLimits:['trial pointer malformed: /a/damaged.json: missing field'],busy:false,act:async()=>{}}));
  assert.match(h,/role="alert" aria-label="Draft workspace limits"/);
  assert.match(h,/trial pointer malformed: \/a\/damaged.json/);
  assert.match(h,/changed transition not reported/);
  const clean=renderToStaticMarkup(React.createElement(WorkflowDraftsView,{data:{...data,transitionLimits:[]},workspace:true,pointerLimits:[],busy:false,act:async()=>{}}));
  assert.doesNotMatch(clean,/Draft workspace limits/);
});
