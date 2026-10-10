import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// Trial and bring-back composers, the review's last clean trial line, and their
// place in the conversation panel (WR TT-3a, TT-3b, TT-10, TT-13; OI-008: the
// host pre-fills and sends; the view sends only on the person's Send press).
const document = installMiniDom();
const React = (await import('react')).default;
const {renderToStaticMarkup} = await import('react-dom/server');
const {createRoot} = await import('react-dom/client');
const {DelegatedTrialComposerView,DelegatedTrialComposer,CleanTrialPanelView,CleanTrialPanel,BringBackComposerView,BringBackComposer,TrialCard,composersFor}=loadSrc('TrialComposer');
const {LastCleanTrialLine}=loadSrc('WorkflowDrafts');
const {ConversationPanel,WorkflowRootPanel}=loadSrc('App');

const g={appSession:'s',home:'h',spawnCounter:1};
const conv=threadId=>({generation:g,threadId,model:'gpt-x',modelProvider:'openai',appRole:{standing:'app-observed',role:null},roleRelation:{kind:'start'},futureGuidanceNotices:[]});
const conversations=[conv('auth'),conv('other')];
const ckey=c=>JSON.stringify([c.generation,c.threadId]);
const h=(c,p)=>renderToStaticMarkup(React.createElement(c,p));
const find=(node,match,found=[])=>{
  if(Array.isArray(node)){for(const n of node)find(n,match,found);return found;}
  if(!node||typeof node!=='object')return found;
  if(typeof node.type==='function')return find(node.type(node.props),match,found);
  if(match(node))found.push(node);
  find(node.props?.children,match,found);return found;
};
const buttons=(tree,name)=>find(tree,n=>n.type==='button'&&renderToStaticMarkup(n).includes(`>${name}</button>`));
const spy=()=>{const calls=[];return {calls,act:async(c,a)=>{calls.push([c,a]);return {ok:true};}};};
const unsent={state:'unsent'};

const pending=(over={})=>({reference:'trial:7',sequence:4,kind:'delegated',draftName:'load-check',location:'project',content:{value:'0123456789abcdef'},rev12:'0123456789ab',
  card:'trial 4 of draft load-check at content 0123456789ab — not registered; not a workflow run',header:'[Chirality] Workflow trial 4 …',text:'[Chirality] Workflow trial 4 of draft project:load-check\nRUN TEXT BODY',
  textIdentity:{value:'feedfacefeedface'},bytes:812,message:'Please try draft load-check (trial 4, content 0123456789ab). Start one sub-agent …',
  authoring:{generation:g,threadId:'auth'},cleanConversation:null,delegation:{reading:'not established',reason:'delegation tools not reported by Codex'},
  runInForce:'resolve-spacing is in force in this conversation; the trial opens no run and resolve-spacing stays in force',draftChanged:'draft changed since this trial text was made; Try again for the current version',
  workFolder:'.chirality/workflow-trials/w1',state:'pre-filled',limit:null,...over});

test('the delegated composer pre-fills the message and shows the card, notes and target, and sends only on Send (TT-3a)',()=>{
  const html=h(DelegatedTrialComposer,{pending:pending(),conversations,busy:false,ready:true,act:async()=>{throw new Error('must not be called while rendering');}});
  assert.match(html,/<textarea[^>]*>Please try draft load-check \(trial 4, content 0123456789ab\)/);
  assert.match(html,/trial 4 of draft load-check at content 0123456789ab — not registered; not a workflow run/);
  assert.match(html,/<details><summary>Open the trial text \(812 bytes; identity feedfacefeed\)<\/summary><pre[^>]*>\[Chirality\] Workflow trial 4 of draft project:load-check\nRUN TEXT BODY<\/pre>/);
  assert.match(html,/to change it, change the draft and Try again/);
  assert.match(html,/Delegation not established: delegation tools not reported by Codex/);
  assert.match(html,/resolve-spacing is in force in this conversation/);
  assert.match(html,/draft changed since this trial text was made/);
  assert.match(html,/<option value="[^"]*" selected="">auth ·/,'defaults to the authoring conversation');
  assert.doesNotMatch(h(DelegatedTrialComposer,{pending:pending({delegation:{reading:'present',reason:''}}),conversations,busy:false,ready:true,act:async()=>{}}),/Delegation present/);
  const s=spy();const outcomes=[];
  const tree=DelegatedTrialComposerView({pending:pending(),conversations,message:'edited message',setMessage:()=>{},target:ckey(conversations[0]),setTarget:()=>{},outcome:unsent,setOutcome:o=>outcomes.push(o),busy:false,ready:true,act:s.act});
  assert.deepEqual(s.calls,[],'nothing is sent by showing the composer');
  buttons(tree,'Send')[0].props.onClick();
  assert.deepEqual(s.calls,[['workflow_trial_send',{reference:'trial:7',generation:g,threadId:'auth',personText:'edited message'}]]);
  assert.deepEqual(outcomes[0],{state:'sending'});
  const other=spy();
  buttons(DelegatedTrialComposerView({pending:pending(),conversations,message:'m',setMessage:()=>{},target:ckey(conversations[1]),setTarget:()=>{},outcome:unsent,setOutcome:()=>{},busy:false,ready:true,act:other.act}),'Send')[0].props.onClick();
  assert.deepEqual(other.calls,[['workflow_trial_send',{reference:'trial:7',generation:g,threadId:'other',personText:'m'}]],'the person may send to another started conversation');
  const noTarget=DelegatedTrialComposerView({pending:pending(),conversations,message:'m',setMessage:()=>{},target:'',setTarget:()=>{},outcome:unsent,setOutcome:()=>{},busy:false,ready:true,act:other.act});
  assert.equal(buttons(noTarget,'Send')[0].props.disabled,true);
});

test('removing the trial card calls only workflow_trial_cancel',()=>{
  const s=spy();
  const tree=DelegatedTrialComposerView({pending:pending(),conversations,message:'m',setMessage:()=>{},target:ckey(conversations[0]),setTarget:()=>{},outcome:unsent,setOutcome:()=>{},busy:false,ready:true,act:s.act});
  buttons(tree,'Remove')[0].props.onClick();
  assert.deepEqual(s.calls,[['workflow_trial_cancel',{reference:'trial:7'}]]);
  const card=spy();buttons(TrialCard({pending:pending(),busy:false,act:card.act}),'Remove')[0].props.onClick();
  assert.deepEqual(card.calls,[['workflow_trial_cancel',{reference:'trial:7'}]]);
});

const roles=JSON.parse(readFileSync(new URL('../src-tauri/resources/instructions/roles.json',import.meta.url),'utf8')).roles;
const roleSet={available:true,roles,defaultRole:null,conversationRoles:['HELP_HUMAN','HELPS_HUMANS','WORKING_ITEMS']};
const entries=[{value:'chatgpt-account',label:'ChatGPT account'}];
const clean=(over={})=>pending({kind:'clean',authoring:null,delegation:null,runInForce:null,draftChanged:null,message:'Inputs for this trial: …',...over});
const choice=(over={})=>({model:'',modelProvider:'',entryId:'',role:'',roleTouched:false,...over});
const cleanView=(p,c,act,setOutcome=()=>{})=>CleanTrialPanelView({pending:p,roleSet,limits:{},entries,modeHomeClass:'account',choice:c,setChoice:()=>{},message:'my inputs',setMessage:()=>{},outcome:unsent,setOutcome,busy:false,ready:true,act});

test('the clean trial panel offers the conversation roles and a model, and stays unsent without a model (TT-3b, FT-3)',()=>{
  const html=h(CleanTrialPanel,{pending:clean(),roleSet,limits:{},entries,modeHomeClass:'account',busy:false,ready:true,act:async()=>{throw new Error('must not be called while rendering');}});
  for(const r of ['HELP_HUMAN','HELPS_HUMANS','WORKING_ITEMS'])assert.match(html,new RegExp(`value="${r}"`));
  assert.doesNotMatch(html,/value="TASK"/,'TASK is not a conversation role');
  assert.match(html,/Not started — no model selected/);
  assert.match(html,/a clean trial is shown, not required/);
  assert.ok(html.indexOf('Open the trial text')<html.indexOf('Inputs for this trial (editable'),'the card comes first, then the inputs');
  assert.match(html,/<textarea[^>]*>Inputs for this trial: …<\/textarea>/);
  const s=spy();
  assert.equal(buttons(cleanView(clean(),choice(),s.act),'Send')[0].props.disabled,true,'nothing chosen, no send');
  assert.equal(buttons(cleanView(clean(),choice({entryId:'chatgpt-account',modelProvider:'openai'}),s.act),'Send')[0].props.disabled,true,'no model, no send');
  assert.equal(buttons(cleanView(clean(),choice({entryId:'chatgpt-account',model:'gpt-x'}),s.act),'Send')[0].props.disabled,true,'no provider, no send');
  assert.equal(buttons(cleanView(clean(),choice({model:'gpt-x',modelProvider:'openai'}),s.act),'Send')[0].props.disabled,true,'no entry, no send');
  buttons(cleanView(clean(),choice({model:'gpt-x',modelProvider:'openai',entryId:'chatgpt-account',role:'HELPS_HUMANS'}),s.act),'Send')[0].props.onClick();
  buttons(cleanView(clean(),choice({model:'gpt-x',modelProvider:'openai',entryId:'chatgpt-account'}),s.act),'Send')[0].props.onClick();
  assert.deepEqual(s.calls,[
    ['workflow_trial_start_clean',{reference:'trial:7',model:'gpt-x',modelProvider:'openai',entryId:'chatgpt-account',modeHomeClass:'account',role:'HELPS_HUMANS',personText:'my inputs'}],
    ['workflow_trial_start_clean',{reference:'trial:7',model:'gpt-x',modelProvider:'openai',entryId:'chatgpt-account',modeHomeClass:'account',role:null,personText:'my inputs'}]]);
});

test('a clean trial whose conversation started but whose message was not sent is retried in that conversation',()=>{
  const s=spy();
  const started=clean({cleanConversation:{generation:g,threadId:'clean-1'},state:'started; trial message not sent'});
  const tree=cleanView(started,choice(),s.act);
  assert.equal(find(tree,n=>n.type==='input'&&n.props.name==='conversation-role').length,0,'no new role or model choice for a started conversation');
  buttons(tree,'Send')[0].props.onClick();
  assert.deepEqual(s.calls,[['workflow_trial_send',{reference:'trial:7',generation:g,threadId:'clean-1',personText:'my inputs'}]]);
});

const bringBack=(over={})=>({id:'bb-1',trial:'trial:7',run:null,target:{generation:g,threadId:'auth'},prompt:'Here is how trial 4 went. Please assess it against the draft …',
  transcript:'[Chirality] Trial 4 of draft load-check @ 0123456789ab: transcript read from Codex history …\nturn 1 …',card:'transcript of trial 4 (sub-agent child-1)',textIdentity:{value:'aa'},bytes:4000,
  shortenings:['turn 2 command output: … 1200 bytes omitted'],includeNative:false,...over});

test('the bring-back composer pre-fills the prompt and transcript card and sends only on Send (TT-10)',()=>{
  const html=h(BringBackComposer,{pending:bringBack(),conversations,busy:false,ready:true,act:async()=>{throw new Error('must not be called while rendering');}});
  assert.match(html,/<textarea[^>]*>Here is how trial 4 went/);
  assert.match(html,/transcript of trial 4 \(sub-agent child-1\)/);
  assert.match(html,/<pre[^>]*>\[Chirality\] Trial 4 of draft load-check @ 0123456789ab: transcript read from Codex history/);
  assert.match(html,/turn 2 command output: … 1200 bytes omitted/);
  assert.match(html,/<option value="[^"]*" selected="">auth ·/);
  const s=spy();
  const tree=BringBackComposerView({pending:bringBack(),conversations,prompt:'assess please',setPrompt:()=>{},target:ckey(conversations[0]),setTarget:()=>{},outcome:unsent,setOutcome:()=>{},busy:false,ready:true,act:s.act});
  assert.deepEqual(s.calls,[]);
  buttons(tree,'Remove')[0].props.onClick();
  assert.deepEqual(s.calls,[['workflow_bring_back_cancel',{id:'bb-1'}]]);
  buttons(tree,'Send')[0].props.onClick();
  assert.deepEqual(s.calls[1],['workflow_bring_back_send',{id:'bb-1',generation:g,threadId:'auth',personText:'assess please'}]);
});

test('mounting and updating the composers sends nothing (no automatic send)',async()=>{
  const calls=[];const act=async(c,a)=>{calls.push([c,a]);return {};};
  const container=document.createElement('div');document.body.appendChild(container);
  const root=createRoot(container);
  const show=p=>React.act(()=>root.render(React.createElement('div',null,
    React.createElement(DelegatedTrialComposer,{pending:p,conversations,busy:false,ready:true,act}),
    React.createElement(CleanTrialPanel,{pending:clean({cleanConversation:{generation:g,threadId:'clean-1'},state:'started; trial message not sent'}),roleSet,limits:{},entries,modeHomeClass:'account',busy:false,ready:true,act}),
    React.createElement(BringBackComposer,{pending:bringBack(),conversations,busy:false,ready:true,act}))));
  await show(pending());
  await show(pending({draftChanged:null}));
  await new Promise(r=>setTimeout(r,0));
  assert.deepEqual(calls,[]);
  await React.act(()=>root.unmount());
});

test('composers appear in the conversation they belong to',()=>{
  const root={pendingTrials:[pending(),clean(),pending({reference:'trial:8',authoring:{generation:g,threadId:'other'}})],pendingBringBacks:[bringBack(),bringBack({id:'bb-2',target:{generation:g,threadId:'other'}})]};
  const forAuth=composersFor(root,conversations[0]);
  assert.deepEqual(forAuth.delegated.map(p=>p.reference),['trial:7']);
  assert.deepEqual(forAuth.clean.map(p=>p.reference),['trial:7']);
  assert.deepEqual(forAuth.bringBacks.map(b=>b.id),['bb-1']);
  assert.deepEqual(composersFor(root,null).delegated,[]);
  const host={state:'ready',generation:g,roleLimits:{account:{roles:[]}},roleSet,threads:conversations,
    workflowRoot:{...root,trialsStartedHere:[{threadId:'auth',trials:[{reference:'trial:7',sequence:4,draftName:'load-check',kind:'delegated'}]}],
      trialConversations:[{threadId:'other',reference:'trial:5',sequence:2,draftName:'load-check',rev12:'0123',header:'Trial 2 of draft load-check at content 0123 — not registered; not a workflow run · authoring conversation auth',fork:false}]}};
  const panel=threadId=>h(ConversationPanel,{host,threadKey:ckey(conv(threadId)),setThreadKey:()=>{},answer:async()=>{},runAct:async()=>{throw new Error('must not be called while rendering');},send:async()=>{},steer:async()=>{},submitAttachments:async()=>{},interrupt:async()=>{},checkPlanMode:async()=>{},codexBusy:false});
  const auth=panel('auth');
  assert.match(auth,/Trial 4 of draft load-check — pre-filled, not sent/);
  assert.match(auth,/Trials started here: trial 4 of draft load-check \(delegated\)/);
  assert.match(auth,/New trial conversation: trial 4 of draft load-check/);
  assert.equal((auth.match(/aria-label="Bring back composer"/g)??[]).length,1);
  const other=panel('other');
  assert.match(other,/Trial 2 of draft load-check at content 0123 — not registered; not a workflow run · authoring conversation auth/);
  assert.doesNotMatch(other,/Trials started here/);
  assert.equal((other.match(/aria-label="Trial composer"/g)??[]).length,1,'only the trial authored here');
});

test('the review shows the last clean trial as information only; Register is enabled or disabled the same in all three readings (TT-13)',()=>{
  const lines={matches:{state:'matches',reading:'Last clean trial: content 0123456789ab — matches the version under review',draftName:'load-check'},
    differs:{state:'differs',reading:'Last clean trial: content 0123456789ab — differs from the version under review',draftName:'load-check'},
    none:{state:'none',reading:'',draftName:'load-check'}};
  assert.match(h(LastCleanTrialLine,{line:lines.matches,busy:false,act:async()=>{}}),/matches the version under review\. Information only/);
  assert.match(h(LastCleanTrialLine,{line:lines.differs,busy:false,act:async()=>{}}),/differs from the version under review/);
  assert.match(h(LastCleanTrialLine,{line:lines.none,busy:false,act:async()=>{}}),/Last clean trial: none/);
  const s=spy();
  find(LastCleanTrialLine({line:lines.differs,busy:false,act:s.act}),n=>n.type==='button')[0].props.onClick();
  assert.deepEqual(s.calls,[['workflow_trial_prepare',{name:'load-check',kind:'clean',generation:null,threadId:null}]]);
  const register=(line,active)=>{
    const review={reference:'review-1',status:{presentation:null,entries:[]},lastCleanTrial:line};
    const html=h(WorkflowRootPanel,{data:{reviews:[review],activeReview:active?'review-1':null},host:{state:'ready',generation:g,threads:[]},act:async()=>{}});
    const m=html.match(/<button[^>]*>Register this review through native A15 confirmation…<\/button>/);
    assert.ok(m,'Register is offered');return m[0];
  };
  for(const active of [true,false]){
    const shown=[lines.matches,lines.differs,lines.none,null].map(l=>register(l,active));
    assert.equal(new Set(shown).size,1,`Register identical across readings (active ${active})`);
    assert.equal(shown[0].includes('disabled'),!active);
  }
  assert.match(h(WorkflowRootPanel,{data:{reviews:[{reference:'review-1',status:{},lastCleanTrial:lines.differs}],activeReview:'review-1'},host:{},act:async()=>{}}),/aria-label="Last clean trial"/);
});
