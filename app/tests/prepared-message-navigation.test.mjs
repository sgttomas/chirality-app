import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';

// Real App/children with controlled IPC, using trial_flows::pending_view and
// project_pending's receiving shapes. This proves the UI join, not native acts.
const g={appSession:'prepared-fixture',home:'original-home',spawnCounter:1};
const key=id=>JSON.stringify([g,id]);
const ref=id=>({generation:g,threadId:id});
const thread=id=>({...ref(id),model:'reported',modelProvider:'configured',appRole:{standing:'app-observed',role:null},roleRelation:{kind:'start'},futureGuidanceNotices:[]});
const pending=(over={})=>({reference:'trial:original',sequence:1,kind:'delegated',draftName:'method',location:'project',content:{value:'draft-bytes'},textIdentity:{value:'trial-bytes'},text:'Original trial text',message:'Original person message',authoring:ref('B'),workFolder:'.chirality/workflow-trials/test',state:'pre-filled',...over});
const feedback=(over={})=>({id:'feedback:original',trial:'trial:clean',sequence:2,draftName:'method',run:null,target:ref('A'),source:{kind:'clean',generation:g,threadId:'B',turn:'trial-turn',standing:'read from original clean trial history'},prompt:'Original feedback prompt',transcript:'Original clean trial B outcome',textIdentity:{value:'feedback-bytes'},includeNative:false,shortenings:[],...over});
const deferred=()=>{let resolve;return {promise:new Promise(yes=>{resolve=yes;}),resolve:v=>resolve(v)};};
const document=installMiniDom();
const React=(await import('react')).default;
const {createRoot}=await import('react-dom/client');
const {App}=loadSrc('App');
const props=e=>e[Object.keys(e).find(k=>k.startsWith('__reactProps$'))];
const elements=(c,tag)=>c.querySelectorAll(e=>e.localName===tag);
const labelled=(c,tag,label)=>elements(c,tag).find(e=>e.parentNode.textContent.startsWith(label));
const region=(c,label)=>c.querySelectorAll(e=>e.getAttribute('aria-label')===label)[0];
const conversation=c=>c.querySelectorAll(e=>e.getAttribute('id')==='conversation')[0];
const visible=e=>{for(let n=e;n;n=n.parentNode)if(props(n)?.hidden)return false;return true;};
const button=(c,label)=>elements(c,'button').find(e=>e.textContent===label&&visible(e));
const frozen={entries:[{name:'frozen-method',workflowText:'FROZEN\nreview text'}],standing:'Frozen reviewed bytes'};
const ordinary='Global unsent text é / 家\n';

async function mounted(options,check){
 const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
 const calls=[],unexpected=[],timers=new Map(),actions=new Set();let timer=0,active='account',nextRead,failRead=false;
 const account={state:'ready',generation:g,threads:['A','B','C','D'].map(thread),roleLimits:{account:{roles:[]}},workflowRoot:{
  context:{sourceRef:'original-workflow-source',generation:g,historyEpoch:1},projectLibraryAvailable:true,
  drafts:{drafts:[{name:'method',state:'draft',content:{value:'draft-bytes'},trials:[]}]},
  selections:[{sourceRef:'original-workflow-source',threadId:'C',selection:{reference:'choice-C',name:'C choice'}}],
  libraries:[],reviews:[{reference:'review:frozen',status:{state:'under review',presentation:frozen}}],activeReview:'review:frozen',
  pendingTrials:options.trials??[pending()],pendingBringBacks:options.feedback??[],
 }};
 const other={state:'ready',generation:{...g,home:'foreign-home'},threads:[{...thread('B'),generation:{...g,home:'foreign-home'}}],workflowRoot:{context:{sourceRef:'foreign-source',generation:{...g,home:'foreign-home'}},pendingTrials:[],pendingBringBacks:[]}};
 const snapshot=()=>structuredClone({...active==='account'?account:other,homeRouting:{activeModeHomeClass:active,entries:[{modeHomeClass:'account'},{modeHomeClass:'api-key'}]}});
 const oldTimers={setInterval:globalThis.setInterval,clearInterval:globalThis.clearInterval};
 globalThis.setInterval=(fn,ms)=>{const id=++timer;timers.set(id,{fn,ms});return id;};globalThis.clearInterval=id=>timers.delete(id);
 const idle=installIdleNativeWaiting(async(command,args)=>{
  calls.push({command,args:structuredClone(args)});
  if(command==='host_status'){
   if(failRead){failRead=false;throw Error('controlled original refresh failure');}
   const value=snapshot(),gate=nextRead;nextRead=undefined;
   if(gate){await gate.promise;return value;}return value;
  }
  if(command==='decision_view')return {rows:[]};
  if(command==='native_confirmation_content')return [{kind:'A15 complete review',digest:'fixture-digest',content:frozen}];
  if(command==='workflow_review_digest')return {digest:'fixture-digest'};
  if(command==='select_home'){active=args.modeHomeClass;return {state:'selected'};}
  if(command==='thread_start'){if(options.startError)throw options.startError;account.threads.push(thread('new-choice'));return {startGeneration:g,result:{thread:{id:'new-choice'}}};}
  if(command==='workflow_trial_send'||command==='workflow_bring_back_send'){
   assert.ok(options.send,'send only in an explicit send-outcome case');return options.send(command,args);
  }
  if(command==='workflow_trial_prepare'){
   assert.ok(options.prepare,'prepare only in the original explicit preparation case');const p=pending();account.workflowRoot.pendingTrials.push(p);return {...p,message:'STALE returned command text must never be displayed'};
  }
  if(command==='workflow_trial_start_clean'){
   assert.equal(options.cleanJourney,true);assert.equal(args.reference,'trial:clean');
   account.workflowRoot.pendingTrials=[];
   account.workflowRoot.drafts.drafts[0].trials=[{reference:'trial:clean',sequence:2,kind:'clean',draftName:'method',authoringConversation:ref('A'),trialConversation:ref('B'),fidelity:{},snapshot:{},standing:'trial, not a run'}];
   return {thread:thread('B')};
  }
  if(command==='workflow_trial_bring_back'){
   assert.equal(options.cleanJourney,true);assert.deepEqual(args,{reference:'trial:clean',generation:g,threadId:'A',includeNative:false});
   account.workflowRoot.pendingBringBacks=[feedback()];return {id:'feedback:original',card:'STALE returned transcript card'};
  }
  unexpected.push({command,args});throw Error(`Unexpected command: ${command}`);
 });
 const track=call=>{if(call?.then){actions.add(call);call.then(()=>actions.delete(call),()=>actions.delete(call));}};
 const change=async(e,value)=>React.act(()=>{assert.ok(e);track(props(e).onChange({target:{value}}));});
 const press=async(label,within=c)=>React.act(()=>{const e=button(within,label);assert.ok(e,label);assert.equal(!!props(e).disabled,false,label);track(props(e).onClick());});
 const poll=async()=>React.act(async()=>{const p=[...timers.values()].find(p=>p.fn.toString().includes('host_status'));assert.ok(p);p.fn();});
 const selected=()=>props(elements(conversation(c),'select')[0]).value;
 const choose=async id=>change(elements(conversation(c),'select')[0],key(id));
 const editChoice=async(value='newer-choice')=>{await change(labelled(c,'input','Model '),value);await change(labelled(c,'input','Configured Codex provider '),'configured');await change(labelled(c,'select','Access entry '),'local-provider');};
 const model=()=>props(labelled(c,'input','Model ')).value;
 const composer=label=>region(conversation(c),label??'Trial composer');
 const assertIndependent=()=>{
  assert.equal(props(labelled(c,'select','Workflow chat ')).value,'C');
  assert.equal(props(labelled(c,'select','Authoring conversation ')).value,key('B'));
  assert.equal(props(labelled(conversation(c),'textarea','Text ')).value,ordinary);
  assert.match(region(c,'Content named by an open native confirmation').textContent,/FROZEN\nreview text/);
  assert.match(c.textContent,/Frozen reviewed bytes/);
 };
 try{
  await React.act(async()=>root.render(React.createElement(App)));
  await choose('A');await change(labelled(conversation(c),'textarea','Text '),ordinary);
  await change(labelled(c,'select','Workflow chat '),'C');await change(labelled(c,'select','Authoring conversation '),key('B'));
  await check({c,calls,account,selected,choose,change,press,poll,composer,assertIndependent,editChoice,model,track,
   gate:()=>{const gate=deferred();nextRead=gate;return gate;},fail:()=>{failRead=true;},snapshot,
   open:(id='B')=>press(`View prepared message in conversation ${id}`)});
  idle.assertClean(c);assert.deepEqual(unexpected,[]);
 }finally{
  const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);assert.equal(timers.size,0);Object.assign(globalThis,oldTimers);
 }
}

test('current pending Open joins operational A, Workflow C and original composer B without losing local target D or edits',async()=>{
 await mounted({},async ui=>{
  await ui.choose('B');const original=ui.composer();await ui.change(elements(original,'textarea')[0],'Person edited trial text');await ui.change(labelled(original,'select','Send to '),key('D'));
  await ui.choose('A');assert.equal(visible(original),false);ui.assertIndependent();const before=ui.calls.length;
  await ui.open();assert.equal(ui.selected(),key('B'));assert.equal(ui.composer(),original,'original mounted composer, not a reconstruction');assert.equal(visible(original),true);
  assert.equal(props(elements(original,'textarea')[0]).value,'Person edited trial text');assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));ui.assertIndependent();
  assert.deepEqual(ui.calls.slice(before).map(c=>c.command),['host_status'],'Open observes only; no sends, preparations, selections, resume or registration');
  await ui.choose('A');await ui.open();assert.equal(ui.composer(),original);ui.assertIndependent();
 });
});

test('original explicit preparation uses current pending authority and preserves the existing no-echo result behavior',async()=>{
 await mounted({trials:[],prepare:true},async ui=>{await ui.press('Try with the authoring agent');assert.equal(ui.selected(),key('A'));assert.doesNotMatch(ui.c.textContent,/STALE returned command text/);assert.match(ui.c.textContent,/Send or remove it in the conversation panel/);await ui.open();assert.equal(ui.selected(),key('B'));assert.equal(props(elements(ui.composer(),'textarea')[0]).value,'Original person message');ui.assertIndependent();});
});

test('library-only inspection and a different current authoring choice remain independent of prepared owner B',async()=>{
 await mounted({},async ui=>{await ui.change(labelled(ui.c,'select','Workflow chat '),'');await ui.change(labelled(ui.c,'select','Authoring conversation '),key('C'));await ui.open();assert.equal(ui.selected(),key('B'));assert.equal(props(labelled(ui.c,'select','Workflow chat ')).value,'');assert.equal(props(labelled(ui.c,'select','Authoring conversation ')).value,key('C'));});
});

test('authoring A → explicit clean trial B → feedback A remains an unsent original composer with local Send target D',async()=>{
 await mounted({cleanJourney:true,trials:[pending({reference:'trial:clean',sequence:2,kind:'clean',authoring:ref('A')})]},async ui=>{
  const clean=region(ui.c,'New trial conversation');assert.ok(visible(clean));assert.equal(button(ui.c,'View prepared message in conversation B'),undefined,'a clean preparation invents no existing B target');
  await ui.change(labelled(clean,'input','Model '),'chosen');await ui.change(labelled(clean,'input','Configured Codex provider '),'configured');await ui.change(labelled(clean,'select','Access entry '),'local-provider');await ui.press('Send',clean);assert.equal(ui.selected(),key('B'));
  await ui.press('Bring trial back');assert.doesNotMatch(ui.c.textContent,/STALE returned transcript card/);assert.equal(ui.selected(),key('B'));
  await ui.open('A');const original=ui.composer('Bring back composer');assert.equal(visible(original),true);await ui.change(elements(original,'textarea')[0],'Edited feedback');await ui.change(labelled(original,'select','Send to '),key('D'));
  await ui.choose('C');const before=ui.calls.length;await ui.open('A');assert.equal(ui.composer('Bring back composer'),original);assert.equal(props(elements(original,'textarea')[0]).value,'Edited feedback');assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));ui.assertIndependent();
  assert.deepEqual(ui.calls.slice(before).map(c=>c.command),['host_status']);assert.equal(ui.calls.filter(c=>c.command==='workflow_bring_back_send').length,0);
 });
});

for(const kind of ['trial','feedback'])test(`${kind} retains pending and late missing send outcome through hide/show and Open`,async()=>{
 const send=deferred();await mounted({trials:kind==='trial'?[pending()]:[pending({authoring:ref('A')})],feedback:kind==='feedback'?[feedback({target:ref('B')})]:[feedback()],send:()=>send.promise},async ui=>{
  await ui.choose('B');const original=ui.composer(kind==='trial'?'Trial composer':'Bring back composer');await ui.change(elements(original,'textarea')[0],'edited before explicit send');await ui.change(labelled(original,'select','Send to '),key('D'));
  await ui.press('Send',original);assert.match(original.textContent,/Sending; waiting/);await ui.open('A');await ui.open();assert.equal(ui.composer(kind==='trial'?'Trial composer':'Bring back composer'),original);assert.match(original.textContent,/Sending; waiting/);
  await ui.open('A');await React.act(async()=>send.resolve(undefined));assert.match(original.textContent,/did not report the send/);await ui.open();assert.match(original.textContent,/did not report the send/);assert.equal(props(elements(original,'textarea')[0]).value,'edited before explicit send');assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));
 });
});

const changes={
 removed:h=>{h.workflowRoot.pendingTrials=[];},
 replaced:h=>{h.workflowRoot.pendingTrials=[pending({textIdentity:{value:'replacement'},message:'Replacement message'})];},
 'same ID foreign owner home':h=>{h.workflowRoot.pendingTrials[0].authoring.generation={...g,home:'foreign-home'};},
 'same ID new owner generation':h=>{h.workflowRoot.pendingTrials[0].authoring.generation={...g,spawnCounter:2};},
 'same ID new source':h=>{h.workflowRoot.context.sourceRef='new-source';},
 'closed source':h=>{h.generationClosed=true;},
 'changed source generation':h=>{h.generation={...g,spawnCounter:2};h.workflowRoot.context.generation=h.generation;},
 'missing exact loaded target':h=>{h.threads=h.threads.filter(t=>t.threadId!=='B');},
 'cold owner reference':h=>{h.workflowRoot.pendingTrials[0].authoring='B';},
};
for(const[name,mutate]of Object.entries(changes))test(`Open refuses ${name} after fresh reobservation, without fallback`,async()=>{
 await mounted({},async ui=>{mutate(ui.account);const before=ui.calls.length;await ui.open();assert.equal(ui.selected(),key('A'));assert.match(ui.c.textContent,/Prepared-message navigation refused/);assert.deepEqual(ui.calls.slice(before).map(c=>c.command),['host_status']);});
});

test('failed refresh refuses without changing the view or retrying preparation/navigation on a later poll',async()=>{
 await mounted({},async ui=>{ui.fail();await ui.open();assert.equal(ui.selected(),key('A'));assert.match(ui.c.textContent,/refresh failed: Error: controlled original refresh failure/);await ui.poll();assert.equal(ui.selected(),key('A'));ui.assertIndependent();});
});

for(const name of ['selection','selection away and back','chooser edit','home','home away and back','Start refused','newer observation','source changed then restored'])test(`delayed Open cannot win over ${name}`,async()=>{
 await mounted({startError:'controlled new Start refusal'},async ui=>{
  if(name==='Start refused')await ui.editChoice();const gate=ui.gate();await ui.open();assert.equal(ui.selected(),key('A'));
  if(name.startsWith('selection')){await ui.choose('D');if(name.endsWith('back'))await ui.choose('A');}
  if(name==='chooser edit')await ui.editChoice();
  if(name.startsWith('home')){await ui.press('Use api-key home');if(name.endsWith('back'))await ui.press('Use account home');}
  if(name==='Start refused')await ui.press('Start thread');
  if(name==='newer observation')await ui.poll();
  if(name==='source changed then restored'){ui.account.workflowRoot.context.sourceRef='changed';await ui.poll();ui.account.workflowRoot.context.sourceRef='original-workflow-source';await ui.poll();}
  await React.act(async()=>gate.resolve());assert.notEqual(ui.selected(),key('B'));assert.match(ui.c.textContent,/Prepared-message navigation refused/);
  if(name==='selection')assert.equal(ui.selected(),key('D'));if(name==='chooser edit')assert.equal(ui.model(),'newer-choice');if(name==='home')assert.match(ui.c.textContent,/Active home class: api-key/);
  await ui.poll();assert.notEqual(ui.selected(),key('B'),'a later poll cannot replay the old Open');
 });
});

test('a replaced pending binding retires edits and late outcomes instead of rebinding them to its reused ID',async()=>{
 const send=deferred();await mounted({send:()=>send.promise},async ui=>{
  await ui.choose('B');const original=ui.composer();await ui.change(elements(original,'textarea')[0],'Old local text');await ui.change(labelled(original,'select','Send to '),key('D'));await ui.press('Send',original);
  changes.replaced(ui.account);await ui.poll();const replacement=ui.composer();assert.notEqual(replacement,original);assert.equal(props(elements(replacement,'textarea')[0]).value,'Replacement message');assert.equal(props(labelled(replacement,'select','Send to ')).value,key('B'));
  await React.act(async()=>send.resolve(undefined));assert.doesNotMatch(replacement.textContent,/did not report the send/);await ui.choose('A');await ui.open();assert.equal(ui.composer(),replacement);
 });
});

// Multiple clean cards stay global, and multiple delegated cards may share B.
// The person's exact clicked pending reference chooses the post-commit reveal.
test('Open reveals the exact original pending composer among global clean cards and multiple B composers, once after commit',async()=>{
 await mounted({trials:[pending({kind:'clean',reference:'trial:global-1'}),pending(),pending({kind:'clean',reference:'trial:global-2'}),pending({reference:'trial:second-B',sequence:3,message:'Second B composer'})]},async ui=>{
  const composers=ui.c.querySelectorAll(e=>e.getAttribute('aria-label')==='Trial composer');
  assert.equal(composers.length,2);const [first,second]=composers;const scrolls=[];
  const cards=ui.c.querySelectorAll(e=>['Trial composer','New trial conversation'].includes(e.getAttribute('aria-label')));
  for(const card of cards)card.parentNode.scrollIntoView=()=>{assert.equal(visible(card),true,'reveal occurs after the target was unhidden');scrolls.push(card);};
  const secondOpen=elements(ui.c,'button').find(e=>e.textContent==='View prepared message in conversation B'&&e.parentNode.textContent.startsWith('Trial 3 '));assert.ok(secondOpen);
  await React.act(()=>props(secondOpen).onClick());assert.equal(ui.selected(),key('B'));assert.deepEqual(scrolls,[second]);assert.equal(ui.composer(),first,'first B composer remains independently mounted');ui.assertIndependent();
  await ui.poll();assert.deepEqual(scrolls,[second],'poll cannot repeat a consumed reveal');
  await ui.choose('A');scrolls.length=0;
  // Inject a newer user selection at the actual DOM unhide commit, before
  // passive effects run. No stale wrapper is then scrolled or focused.
  const chooser=elements(conversation(ui.c),'select')[0];
  const wrapper=second.parentNode,remove=wrapper.removeAttribute;let supersededAtCommit=false;
  wrapper.removeAttribute=function(name){remove.call(this,name);if(name==='hidden'&&!supersededAtCommit){supersededAtCommit=true;props(chooser).onChange({target:{value:key('D')}});}};
  await React.act(()=>props(secondOpen).onClick());wrapper.removeAttribute=remove;
  assert.equal(supersededAtCommit,true,'the new selection was injected after Open selected B, at commit');
  assert.equal(ui.selected(),key('D'));assert.deepEqual(scrolls,[]);assert.match(ui.c.textContent,/exact composer reveal was superseded/);
 });
});

test('a late older Open cannot replace a newer successful notice or reveal',async()=>{
 await mounted({feedback:[feedback()]},async ui=>{
  const scrolls=[];for(const card of ui.c.querySelectorAll(e=>['Trial composer','Bring back composer'].includes(e.getAttribute('aria-label'))))card.parentNode.scrollIntoView=()=>scrolls.push(card);
  const gate=ui.gate();await ui.open('B');await ui.open('A');assert.equal(ui.selected(),key('A'));assert.equal(scrolls.length,1);assert.match(ui.c.textContent,/Prepared composer shown \(original-workflow-source, conversation A/);
  await React.act(async()=>gate.resolve());assert.equal(ui.selected(),key('A'));assert.equal(scrolls.length,1);assert.match(ui.c.textContent,/Prepared composer shown \(original-workflow-source, conversation A/);assert.doesNotMatch(ui.c.textContent,/Prepared-message navigation refused/);
 });
});

for(const[name,mutate]of Object.entries({
 removed:h=>{h.workflowRoot.pendingBringBacks=[];},
 'replaced transcript':h=>{h.workflowRoot.pendingBringBacks[0].transcript='Replacement transcript';},
 'same ID new source generation':h=>{h.workflowRoot.pendingBringBacks[0].source.generation={...g,spawnCounter:2};},
 'same ID foreign owner':h=>{h.workflowRoot.pendingBringBacks[0].target.generation={...g,home:'foreign-home'};},
}))test(`Bring-back Open refuses ${name} instead of substituting an original authoring default`,async()=>{
 await mounted({trials:[],feedback:[feedback({target:ref('B')})]},async ui=>{mutate(ui.account);await ui.open('B');assert.equal(ui.selected(),key('A'));assert.match(ui.c.textContent,/Prepared-message navigation refused/);assert.equal(ui.calls.filter(c=>c.command==='workflow_bring_back_send').length,0);});
});

test('stale captured click refuses a retired pending item before reading or navigating',async()=>{
 await mounted({},async ui=>{const click=props(button(ui.c,'View prepared message in conversation B')).onClick;changes.removed(ui.account);await ui.poll();const before=ui.calls.length;await React.act(()=>click());assert.equal(ui.selected(),key('A'));assert.match(ui.c.textContent,/original prepared message is missing/);assert.deepEqual(ui.calls.slice(before),[]);});
});

test('new same bare ID in another home and generation does not inherit original composer edits',async()=>{
 await mounted({},async ui=>{
  await ui.choose('B');const original=ui.composer();await ui.change(elements(original,'textarea')[0],'Original edited draft');await ui.change(labelled(original,'select','Send to '),key('D'));
  const next={...g,home:'replacement-home',spawnCounter:2};ui.account.generation=next;ui.account.threads=ui.account.threads.map(row=>({...row,generation:next}));ui.account.workflowRoot.context={sourceRef:'replacement-source',generation:next};ui.account.workflowRoot.pendingTrials=[pending({authoring:{generation:next,threadId:'B'}})];
  await ui.poll();await ui.open();const replacement=ui.composer();assert.notEqual(replacement,original);assert.equal(props(elements(replacement,'textarea')[0]).value,'Original person message');assert.equal(props(labelled(replacement,'select','Send to ')).value,JSON.stringify([next,'B']));
 });
});

for(const outcome of ['acknowledged','refused'])test(`a late ${outcome} trial send retains its actual outcome through Open and failed observation`,async()=>{
 const gate=deferred();await mounted({feedback:[feedback()],send:async()=>{await gate.promise;if(outcome==='refused')throw {message:'Original send refused; message retained',prefillKept:true};return {threadId:'D'};}},async ui=>{
  await ui.choose('B');const original=ui.composer();await ui.change(labelled(original,'select','Send to '),key('D'));await ui.press('Send',original);await ui.open('A');ui.fail();
  await React.act(async()=>gate.resolve());await ui.open();assert.equal(ui.composer(),original);
  if(outcome==='acknowledged'){assert.match(original.textContent,/Sent to conversation D/);assert.doesNotMatch(original.textContent,/refresh failure/);}
  else{assert.match(original.textContent,/Original send refused; message retained/);assert.match(original.textContent,/You can send it again/);}
  assert.match(ui.c.textContent,/view refresh unavailable/);
 });
});
