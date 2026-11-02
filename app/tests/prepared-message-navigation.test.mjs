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
const deferred=()=>{let resolve,reject;return {promise:new Promise((yes,no)=>{resolve=yes;reject=no;}),resolve:v=>resolve(v),reject:e=>reject(e)};};
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
const nativePath=path=>({encoding:'unix_bytes',bytes:[...new TextEncoder().encode(path)]});
const fixedProject='/invented/Fixed App project / 家';
const libraryPath='/invented/Opened user library / é';

async function mounted(options,check){
 const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
 const previousGetById=document.getElementById;
 document.getElementById=id=>c.querySelectorAll(node=>node.getAttribute('id')===id)[0]??null;
 const calls=[],unexpected=[],timers=new Map(),actions=new Set();let timer=0,active='account',nextRead,failRead=false;
 const account={state:'ready',generation:g,threads:['A','B','C','D'].map(thread),roleLimits:{account:{roles:[]}},
 currentAppProjectContext:{reference:fixedProject,sourceCaption:'configured App directory',standing:'explicit frozen Root observation; no native/actor authority inferred'},currentAppProjectContextLimit:null,
 attachmentSelections:{launchAppProjectObservation:{source:'explicit App launch CHIRALITY_WORKSPACE',nativeRoot:nativePath(fixedProject),associationStanding:'launch source only; no accepted REC context/persistent thread-project binding established by this picker'}},
 workflowRoot:{
  context:{sourceRef:'original-workflow-source',generation:g,historyEpoch:1},projectLibraryAvailable:true,
  drafts:{drafts:[{name:'method',state:'draft',content:{value:'draft-bytes'},trials:[]}]},
  selections:[{sourceRef:'original-workflow-source',threadId:'C',selection:{reference:'choice-C',name:'C choice'}}],
  libraries:[{reference:'library:opened',root:nativePath(libraryPath),origin:'user',sourceRoot:libraryPath,registered:[]}],activeLibrary:'library:opened',reviews:[{reference:'review:frozen',status:{state:'under review',presentation:frozen}}],activeReview:'review:frozen',
  pendingTrials:options.trials??[pending()],pendingBringBacks:options.feedback??[],
 }};
 const other={state:'ready',generation:{...g,home:'foreign-home'},threads:[{...thread('B'),generation:{...g,home:'foreign-home'}}],workflowRoot:{context:{sourceRef:'foreign-source',generation:{...g,home:'foreign-home'}},pendingTrials:[],pendingBringBacks:[]}};
 const snapshot=()=>{const home=active==='account'?account:other;return structuredClone({...home,
  currentAppProjectContext:account.currentAppProjectContext,currentAppProjectContextLimit:account.currentAppProjectContextLimit,
  attachmentSelections:account.attachmentSelections,
  workflowRoot:{...home.workflowRoot,libraries:account.workflowRoot.libraries,activeLibrary:account.workflowRoot.activeLibrary},
  homeRouting:{activeModeHomeClass:active,entries:[{modeHomeClass:'account'},{modeHomeClass:'api-key'}]}});};
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
  if(command==='open_waiting_requests'){
   assert.ok(options.waiting,'waiting navigation only in its explicit source-bound case');
   assert.deepEqual(args,options.waiting);active=args.modeHomeClass;return {...args,threadLoaded:args.threadId!==null};
  }
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
 // A native select emits change only when an available option changes value.
 // Selecting its already-selected No-chat option cannot acknowledge lost state.
 const pickWorkflowChat=async value=>{
  const select=labelled(c,'select','Workflow chat ');assert.ok(select);assert.equal(!!props(select).disabled,false);
  assert.ok(elements(select,'option').some(option=>props(option).value===value),'the chosen option must actually exist');
  if(props(select).value===value)return false;
  await change(select,value);return true;
 };
 const press=async(label,within=c)=>React.act(()=>{
  const e=button(within,label);assert.ok(e,label);assert.equal(!!props(e).disabled,false,label);
  // Expose an existing control through its native disclosure before pressing
  // it. This never reveals a composer's hidden foreign render owner.
  for(let parent=e.parentNode;parent;parent=parent.parentNode)if(parent.localName==='details'&&parent.getAttribute('class')==='workspace-disclosure')parent.open=true;
  track(props(e).onClick());
 });
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
  options.beforeMount?.(account,other);
  await React.act(async()=>root.render(React.createElement(App)));
  if(options.initialize!==false){
   await choose('A');await change(labelled(conversation(c),'textarea','Text '),ordinary);
   await pickWorkflowChat('C');await change(labelled(c,'select','Authoring conversation '),key('B'));
  }
  await check({c,calls,account,other,selected,choose,change,pickWorkflowChat,press,poll,composer,assertIndependent,editChoice,model,track,
   gate:()=>{const gate=deferred();nextRead=gate;return gate;},fail:()=>{failRead=true;},snapshot,
   open:(id='B')=>press(`View prepared message in conversation ${id}`)});
  idle.assertClean(c);assert.deepEqual(unexpected,[]);
 }finally{
  const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);assert.equal(timers.size,0);Object.assign(globalThis,oldTimers);document.getElementById=previousGetById;
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
 await mounted({},async ui=>{await ui.pickWorkflowChat('');await ui.change(labelled(ui.c,'select','Authoring conversation '),key('C'));await ui.open();assert.equal(ui.selected(),key('B'));assert.equal(props(labelled(ui.c,'select','Workflow chat ')).value,'');assert.equal(props(labelled(ui.c,'select','Authoring conversation ')).value,key('C'));});
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

const startResult=c=>elements(c,'p').find(e=>e.textContent.startsWith('thread_start:'))?.textContent;
for(const supersession of ['newer Start','workflow source','home'])test(`old trial observer failure keeps its original attribution after ${supersession}`,async()=>{
 await mounted({send:async()=>({threadId:'D'})},async ui=>{
  await ui.choose('B');const original=ui.composer();await ui.change(labelled(original,'select','Send to '),key('D'));await ui.editChoice();
  const observation=ui.gate();await ui.press('Send',original);assert.match(original.textContent,/Sending; waiting/);
  if(supersession==='workflow source'){ui.account.workflowRoot.context.sourceRef='replacement-workflow-source';await ui.poll();}
  if(supersession==='home'){await ui.press('Use api-key home');}
  else await ui.press('Start thread');
  const newer=startResult(ui.c),before=ui.calls.length;
  if(supersession!=='home')assert.match(newer,/new-choice/);
  await React.act(async()=>observation.reject(Error('Original trial observer rejected late')));
  assert.equal(startResult(ui.c),newer,'old observation must not append to or replace the newer global result');
  const limit=region(ui.c,'Trial view observation limit');assert.ok(limit,'the observer failure retains a separately identified original subject');
  assert.match(limit.textContent,/workflow_trial_send/);assert.match(limit.textContent,/trial:original/);assert.match(limit.textContent,/attempt 1/);
  assert.match(limit.textContent,/original-workflow-source/);assert.match(limit.textContent,/original-home/);assert.match(limit.textContent,/prepared-fixture/);assert.match(limit.textContent,/"spawnCounter":1/);assert.match(limit.textContent,/Original trial observer rejected late/);
  assert.match(limit.textContent,/"threadId":"D"/,'the requested Send target is captured separately from the original render owner B');
  assert.doesNotMatch(limit.textContent,/replacement-workflow-source|foreign-home|new-choice/);
  if(supersession==='newer Start'){assert.equal(ui.composer(),original);assert.match(original.textContent,/Sent to conversation D/);}
  if(supersession==='workflow source'){assert.notEqual(ui.composer(),original);assert.doesNotMatch(ui.composer().textContent,/Sent to conversation D/,'retired outcome cannot populate the same bare ID under the replacement source');}
  assert.deepEqual(ui.calls.slice(before),[],'settling the observer never retries or sends');
 });
});

test('older trial observation cannot relabel a newer overlapping trial attempt with the same command result',async()=>{
 await mounted({trials:[pending(),pending({reference:'trial:second',sequence:2})],send:async()=>({threadId:'D'})},async ui=>{
  await ui.choose('B');const composers=ui.c.querySelectorAll(e=>e.getAttribute('aria-label')==='Trial composer');assert.equal(composers.length,2);
  for(const composer of composers)await ui.change(labelled(composer,'select','Send to '),key('D'));
  const sends=composers.map(composer=>props(button(composer,'Send')).onClick),observation=ui.gate();
  // Both explicit presses were queued while their distinct composers were
  // enabled. Their command results happen to be identical; attempts are not.
  await React.act(()=>{sends[0]();sends[1]();});
  assert.equal(ui.calls.filter(c=>c.command==='workflow_trial_send').length,2);assert.match(composers[1].textContent,/Sent to conversation D/);
  await React.act(async()=>observation.reject(Error('Older trial-only observer failure')));
  assert.match(composers[0].textContent,/Sent to conversation D/);assert.match(composers[1].textContent,/Sent to conversation D/);
  assert.equal(region(ui.c,'Trial view observation limit'),undefined,'the latest successful trial attempt has no old observer limit');
  assert.doesNotMatch(ui.c.textContent,/Older trial-only observer failure/);
 });
});

const working=c=>region(c,'Workflow working context');
const contextText=(c,label)=>region(c,label)?.textContent??'';
const ownerIn=c=>contextText(c,'Original composer owner');
const assertChoice=(c,label,id)=>assert.match(contextText(c,label),new RegExp(`${label}: Conversation ${id}(?:Exact|$)`));

test('working context keeps project/library, operational A, Workflow C, authoring B and prepared owner B distinct from local Send D',async()=>{
 await mounted({},async ui=>{
  assert.equal(contextText(ui.c,'Fixed App project display'),fixedProject,'the matching launch-native projection supplies a readable primary project folder');assert.ok(working(ui.c).textContent.includes(fixedProject));assert.ok(working(ui.c).textContent.includes(libraryPath));
  assertChoice(ui.c,'Operational conversation viewed','A');assertChoice(ui.c,'Workflow chat context','C');assertChoice(ui.c,'Authoring choice for new trials','B');assert.match(ownerIn(working(ui.c).parentNode),/Conversation B/);
  const before=ui.calls.length;await ui.choose('B');const original=ui.composer();await ui.change(elements(original,'textarea')[0],'Retained edited working-context draft');await ui.change(labelled(original,'select','Send to '),key('D'));await ui.choose('A');
  assert.equal(ui.calls.length,before,'read-only context and selector rendering issues no RPC');assert.match(ownerIn(original.parentNode),/Conversation B/);assert.doesNotMatch(ownerIn(original.parentNode),/Conversation D/);ui.assertIndependent();
  await ui.open();assert.equal(ui.composer(),original);assertChoice(ui.c,'Operational conversation viewed','B');assertChoice(ui.c,'Workflow chat context','C');assertChoice(ui.c,'Authoring choice for new trials','B');
  assert.equal(props(elements(original,'textarea')[0]).value,'Retained edited working-context draft');assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));ui.assertIndependent();
  const afterOpen=ui.calls.length;await ui.choose('D');await ui.pickWorkflowChat('A');await ui.change(labelled(ui.c,'select','Authoring conversation '),key('C'));
  assertChoice(ui.c,'Operational conversation viewed','D');assertChoice(ui.c,'Workflow chat context','A');assertChoice(ui.c,'Authoring choice for new trials','C');assert.match(ownerIn(original.parentNode),/Conversation B/);
  assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));assert.equal(ui.composer(),original);assert.equal(ui.calls.length,afterOpen);
  await ui.pickWorkflowChat('');assert.match(contextText(ui.c,'Workflow chat context'),/No chat — library inspection/);assertChoice(ui.c,'Operational conversation viewed','D');assertChoice(ui.c,'Authoring choice for new trials','C');
 });
});

test('opened library and fixed project remain Root observations through library edits, supplier closure and home changes',async()=>{
 await mounted({},async ui=>{
  await ui.choose('B');const original=ui.composer();await ui.change(elements(original,'textarea')[0],'Retained through read-only context changes');await ui.change(labelled(original,'select','Send to '),key('D'));
  ui.account.workflowRoot.libraries.push({reference:'library:second',root:nativePath('/invented/Second project library'),origin:'project',sourceRoot:'/invented/Second project library',registered:[]});ui.account.workflowRoot.activeLibrary='library:second';await ui.poll();
  assert.match(working(ui.c).textContent,/Second project library/);assert.ok(working(ui.c).textContent.includes(fixedProject));assertChoice(ui.c,'Workflow chat context','C');assertChoice(ui.c,'Authoring choice for new trials','B');assert.equal(ui.composer(),original);
  ui.account.generationClosed=true;await ui.poll();for(const label of ['Operational conversation viewed','Workflow chat context','Authoring choice for new trials'])assert.match(contextText(ui.c,label),/Unavailable/);
  assert.match(ownerIn(original.parentNode),/Unavailable/);assert.match(working(ui.c).textContent,/Second project library/);assert.ok(working(ui.c).textContent.includes(fixedProject));assert.equal(ui.composer(),original);assert.equal(props(elements(original,'textarea')[0]).value,'Retained through read-only context changes');assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));
  await ui.press('Use api-key home');assert.match(working(ui.c).textContent,/Second project library/);assert.ok(working(ui.c).textContent.includes(fixedProject));assert.match(contextText(ui.c,'Authoring choice for new trials'),/Unavailable/);
 });
});

for(const replacement of [{...g,home:'foreign-home'},{...g,spawnCounter:2}])test(`same bare B in ${replacement.home==='foreign-home'?'foreign home':'new generation'} supplies no current authoring or owner context`,async()=>{
 await mounted({},async ui=>{
  ui.account.threads=ui.account.threads.map(row=>row.threadId==='B'?{...row,generation:replacement}:row);await ui.poll();
  assertChoice(ui.c,'Operational conversation viewed','A');assertChoice(ui.c,'Workflow chat context','C');assert.match(contextText(ui.c,'Authoring choice for new trials'),/Unavailable/);assert.match(ownerIn(working(ui.c).parentNode),/Unavailable/);
  assert.ok(working(ui.c).textContent.includes(fixedProject));assert.ok(working(ui.c).textContent.includes(libraryPath));
 });
});

test('new native generation qualifies old selector references instead of relabelling them to same-ID chats or calling them no-chat inspection',async()=>{
 await mounted({},async ui=>{
  const next={...g,spawnCounter:2};ui.account.generation=next;ui.account.workflowRoot.context.generation=next;ui.account.threads=ui.account.threads.map(row=>({...row,generation:next}));await ui.poll();
  for(const label of ['Operational conversation viewed','Workflow chat context','Authoring choice for new trials'])assert.match(contextText(ui.c,label),/Unavailable/);
  assert.doesNotMatch(contextText(ui.c,'Workflow chat context'),/No chat — library inspection/);assert.match(ownerIn(working(ui.c).parentNode),/Unavailable/);
  assert.ok(working(ui.c).textContent.includes(fixedProject));assert.ok(working(ui.c).textContent.includes(libraryPath));
  assert.equal(await ui.pickWorkflowChat(''),false);await ui.press('Use No chat — inspect library content');assert.match(contextText(ui.c,'Workflow chat context'),/No chat — library inspection/);
  await ui.change(labelled(ui.c,'select','Authoring conversation '),JSON.stringify([next,'B']));assertChoice(ui.c,'Authoring choice for new trials','B');assert.match(ownerIn(working(ui.c).parentNode),/Unavailable/,'original pending owner is still the earlier generation');
 });
});

test('workflow source loss qualifies its selectors while preserving independent operational, project and opened-library context',async()=>{
 await mounted({},async ui=>{
  ui.account.workflowRoot.context.sourceRef='replacement-workflow-source';await ui.poll();assertChoice(ui.c,'Operational conversation viewed','A');assert.match(contextText(ui.c,'Workflow chat context'),/Unavailable/);assert.match(contextText(ui.c,'Authoring choice for new trials'),/Unavailable/);
  assert.ok(working(ui.c).textContent.includes(fixedProject));assert.ok(working(ui.c).textContent.includes(libraryPath));
  delete ui.account.workflowRoot.context.sourceRef;await ui.poll();assert.equal(await ui.pickWorkflowChat(''),false);await ui.press('Use No chat — inspect library content');assert.match(contextText(ui.c,'Workflow chat context'),/Unavailable/);assert.doesNotMatch(contextText(ui.c,'Workflow chat context'),/No chat — library inspection/);
 });
});

test('unavailable project/library context is explicit and never inferred from availability, library, native cwd or another observation',async()=>{
 await mounted({},async ui=>{
  ui.account.currentAppProjectContext={reference:null,sourceCaption:'App project not established'};ui.account.currentAppProjectContextLimit='Original project association unavailable';
  ui.account.threads[0].cwd='/invented/Native cwd must not become project';ui.account.workflowRoot.projectLibraryAvailable=true;await ui.poll();
  assert.match(working(ui.c).textContent,/Fixed App projectUnavailable — Original project association unavailable/);assert.ok(working(ui.c).textContent.includes(libraryPath));assert.doesNotMatch(working(ui.c).textContent,/Native cwd must not become project/);
  ui.account.currentAppProjectContext={reference:fixedProject,sourceCaption:'configured App directory'};ui.account.currentAppProjectContextLimit=null;ui.account.workflowRoot.activeLibrary='library:missing';await ui.poll();
  assert.ok(working(ui.c).textContent.includes(fixedProject));assert.match(working(ui.c).textContent,/Opened workflow libraryUnavailable — active library reference/);
  ui.account.workflowRoot.activeLibrary=null;await ui.poll();assert.match(working(ui.c).textContent,/No library opened/);assertChoice(ui.c,'Operational conversation viewed','A');assertChoice(ui.c,'Workflow chat context','C');assertChoice(ui.c,'Authoring choice for new trials','B');
 });
});

test('clean composer context stays global and library inspection works before a native generation exists',async()=>{
 await mounted({trials:[pending({kind:'clean'})]},async ui=>{
  assert.match(ownerIn(region(ui.c,'New trial conversation').parentNode),/global clean composer; no conversation render owner/);assert.equal(button(ui.c,'View prepared message in conversation B'),undefined);
  ui.account.state='absent';ui.account.generation=null;ui.account.workflowRoot.context.generation=null;ui.account.threads=[];await ui.poll();assert.equal(await ui.pickWorkflowChat(''),false);await ui.press('Use No chat — inspect library content');
  assert.match(contextText(ui.c,'Workflow chat context'),/No chat — library inspection/);assert.match(contextText(ui.c,'Operational conversation viewed'),/Unavailable/);assert.ok(working(ui.c).textContent.includes(fixedProject));assert.ok(working(ui.c).textContent.includes(libraryPath));
 });
});

for(const route of ['source','home'])test(`returning original ${route} cannot resurrect a cleared Workflow chat label over the actual No-chat selector`,async()=>{
 await mounted({},async ui=>{
  const select=()=>labelled(ui.c,'select','Workflow chat ');assert.equal(props(select()).value,'C');assertChoice(ui.c,'Workflow chat context','C');
  if(route==='source'){ui.account.workflowRoot.context.sourceRef='temporary-other-source';await ui.poll();ui.account.workflowRoot.context.sourceRef='original-workflow-source';await ui.poll();}
  else{await ui.press('Use api-key home');await ui.press('Use account home');}
  assert.equal(props(select()).value,'','existing selector semantics clear the chat on source/home change');
  assert.match(contextText(ui.c,'Workflow chat context'),/Unavailable/,'a cleared prior chat is not the currently selected chat');
  assert.doesNotMatch(contextText(ui.c,'Workflow chat context'),/Workflow chat context: Conversation C|No chat — library inspection/,'retired choice is distinct from explicit No-chat inspection');
  assertChoice(ui.c,'Operational conversation viewed','A');assertChoice(ui.c,'Authoring choice for new trials','B');
  assert.equal(props(labelled(conversation(ui.c),'textarea','Text ')).value,ordinary);assert.match(region(ui.c,'Content named by an open native confirmation').textContent,/FROZEN\nreview text/);
  await ui.choose('B');const original=ui.composer();await ui.change(elements(original,'textarea')[0],'Preserved through local No-chat acknowledgement');await ui.change(labelled(original,'select','Send to '),key('D'));await ui.choose('A');
  const before=ui.calls.length;assert.equal(await ui.pickWorkflowChat(''),false);await ui.press('Use No chat — inspect library content');assert.equal(props(select()).value,'');assert.match(contextText(ui.c,'Workflow chat context'),/No chat — library inspection/);assert.equal(ui.calls.length,before,'explicit local acknowledgement and summary add no RPC');
  assert.equal(button(ui.c,'Use No chat — inspect library content'),undefined,'acknowledged local state needs no recovery action');assertChoice(ui.c,'Operational conversation viewed','A');assertChoice(ui.c,'Authoring choice for new trials','B');assert.equal(ui.composer(),original);assert.equal(props(elements(original,'textarea')[0]).value,'Preserved through local No-chat acknowledgement');assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));
 });
});

test('project folder display requires exact source correspondence and never decodes an opaque reference',async()=>{
 await mounted({},async ui=>{
  assert.equal(contextText(ui.c,'Fixed App project display'),fixedProject);
  ui.account.attachmentSelections.launchAppProjectObservation.nativeRoot=nativePath('/invented/Unrelated launch observation');await ui.poll();
  assert.match(contextText(ui.c,'Fixed App project display'),/folder display unavailable/);assert.doesNotMatch(contextText(ui.c,'Fixed App project display'),/Unrelated launch observation/);assert.ok(working(ui.c).textContent.includes(fixedProject),'the exact known Root reference remains inspectable');
  delete ui.account.attachmentSelections;await ui.poll();assert.match(contextText(ui.c,'Fixed App project display'),/folder display unavailable/);
  const native={bytes:[47,112,255],encoding:'unix_bytes'};ui.account.currentAppProjectContext.reference=JSON.stringify(native);
  ui.account.attachmentSelections={launchAppProjectObservation:{source:'explicit App launch CHIRALITY_WORKSPACE',nativeRoot:native,associationStanding:'launch source only; no accepted REC binding'}};await ui.poll();
  assert.match(contextText(ui.c,'Fixed App project display'),/path is not valid UTF-8/);assert.match(contextText(ui.c,'Fixed App project display'),/\\xff/);assert.doesNotMatch(contextText(ui.c,'Fixed App project display'),/"bytes"|"encoding"/);
  ui.account.currentAppProjectContextLimit='Fixed project context unavailable';await ui.poll();assert.match(contextText(ui.c,'Fixed App project display'),/Unavailable — Fixed project context unavailable/);assert.doesNotMatch(contextText(ui.c,'Fixed App project display'),/\\xff/);
 });
});

for(const reset of ['source','home','generation'])test(`lost Workflow chat after ${reset} reset supports direct local No-chat recovery with zero available chats`,async()=>{
 await mounted({},async ui=>{
  if(reset==='source'){ui.account.workflowRoot.context.sourceRef='new-workflow-source';ui.account.threads=[];await ui.poll();}
  else if(reset==='home'){ui.other.threads=[];await ui.press('Use api-key home');}
  else{const next={...g,spawnCounter:2};ui.account.generation=next;ui.account.workflowRoot.context.generation=next;ui.account.threads=[];await ui.poll();}
  const select=labelled(ui.c,'select','Workflow chat ');
  assert.equal(props(select).value,'');assert.deepEqual(elements(select,'option').map(option=>props(option).value),[''],'no unrelated chat is available as a workaround');
  assert.match(contextText(ui.c,'Workflow chat context'),/Unavailable/);
  assert.equal(await ui.pickWorkflowChat(''),false,'reselecting the same native option emits no change');assert.match(contextText(ui.c,'Workflow chat context'),/Unavailable/,'unchanged-value selection cannot acknowledge the lost choice');
  const before=ui.calls.length;await ui.press('Use No chat — inspect library content');
  assert.equal(props(select).value,'');assert.match(contextText(ui.c,'Workflow chat context'),/No chat — library inspection/);assert.doesNotMatch(contextText(ui.c,'Workflow chat context'),/Conversation C|Unavailable/);
  assert.equal(ui.calls.length,before,'the explicit recovery is a local acknowledgement only');assert.equal(props(labelled(conversation(ui.c),'textarea','Text ')).value,ordinary);assert.match(region(ui.c,'Content named by an open native confirmation').textContent,/FROZEN\nreview text/);
 });
});

test('local No-chat acknowledgement preserves the current composer and its pending then late send outcome',async()=>{
 const send=deferred();await mounted({send:()=>send.promise},async ui=>{
  ui.account.workflowRoot.context.sourceRef='temporary-source';await ui.poll();ui.account.workflowRoot.context.sourceRef='original-workflow-source';await ui.poll();
  await ui.choose('B');const original=ui.composer();await ui.change(elements(original,'textarea')[0],'Current composer edit');await ui.change(labelled(original,'select','Send to '),key('D'));await ui.press('Send',original);assert.match(original.textContent,/Sending; waiting/);
  const before=ui.calls.length;await ui.press('Use No chat — inspect library content');assert.equal(ui.calls.length,before,'acknowledgement issues no command');assert.equal(ui.composer(),original);assert.match(original.textContent,/Sending; waiting/);assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));
  assertChoice(ui.c,'Operational conversation viewed','B');assertChoice(ui.c,'Authoring choice for new trials','B');assert.match(ownerIn(original.parentNode),/Conversation B/);assert.match(contextText(ui.c,'Workflow chat context'),/No chat — library inspection/);
  await React.act(async()=>send.resolve({threadId:'D'}));assert.equal(ui.composer(),original);assert.match(original.textContent,/Sent to conversation D/);assert.equal(props(elements(original,'textarea')[0]).value,'Current composer edit');assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));
  assert.equal(props(labelled(conversation(ui.c),'textarea','Text ')).value,ordinary);assert.match(region(ui.c,'Content named by an open native confirmation').textContent,/FROZEN\nreview text/);assert.match(contextText(ui.c,'Workflow chat context'),/No chat — library inspection/);
 });
});

const byId=(c,id)=>c.querySelectorAll(e=>e.getAttribute('id')===id)[0];
const disclosureOpen=e=>e.open??e.hasAttribute('open');
const displayed=e=>{for(let n=e;n;n=n.parentNode){if(props(n)?.hidden)return false;if(n!==e&&n.localName==='details'&&!disclosureOpen(n))return false;}return true;};
async function toggleDisclosure(c,id,open){await React.act(()=>{const e=byId(c,id);assert.equal(e?.localName,'details',id);e.open=open;});}
async function followWorkspaceLink(c,label){
 const anchor=elements(c,'a').find(e=>e.textContent===label);assert.ok(anchor,label);assert.ok(displayed(anchor),label);
 const main=elements(c,'main')[0];await React.act(()=>props(main).onClick({target:anchor,currentTarget:main}));
}

test('daily workspace keeps A/C/B/D, exact composer, chooser, global draft and late outcomes through secondary disclosures and Open',async()=>{
 const send=deferred();await mounted({send:()=>send.promise},async ui=>{
  await followWorkspaceLink(ui.c,'New conversation');assert.equal(disclosureOpen(byId(ui.c,'workspace-start')),true);await ui.editChoice('Unsent new-conversation model');await toggleDisclosure(ui.c,'workspace-start',false);await ui.choose('B');const original=ui.composer();await ui.change(elements(original,'textarea')[0],'Edited daily-workspace message');await ui.change(labelled(original,'select','Send to '),key('D'));await ui.choose('A');
  const review=region(ui.c,'Content named by an open native confirmation');const tools=byId(ui.c,'workspace-tools');assert.ok(tools);const panels=tools.querySelectorAll(e=>e.localName==='details'&&e.getAttribute('class')==='workspace-disclosure');assert.ok(panels.length);
  const filePanel=byId(ui.c,'file-acts');const name=elements(byId(ui.c,'workspace-evidence'),'input').find(e=>e.parentNode.textContent.startsWith('Your name on acts'));
  await toggleDisclosure(ui.c,'workspace-files',true);const scope=labelled(filePanel,'input','Scope ');await ui.change(scope,'Unsent file-review scope');
  await toggleDisclosure(ui.c,'workspace-evidence',true);await ui.change(name,'Unsent local name');const before=ui.calls.length;
  for(const panel of panels){await toggleDisclosure(ui.c,panel.getAttribute('id'),true);await toggleDisclosure(ui.c,panel.getAttribute('id'),false);}
  assert.equal(ui.calls.length,before,'disclosure navigation performs no RPC');assert.equal(ui.composer(),original);assert.equal(byId(ui.c,'file-acts'),filePanel);assert.equal(props(scope).value,'Unsent file-review scope','the secondary child retains its own local state');assert.equal(props(name).value,'Unsent local name');assert.equal(ui.model(),'Unsent new-conversation model');ui.assertIndependent();assert.ok(displayed(review),'native confirmation is outside secondary disclosures');
  await followWorkspaceLink(ui.c,'More tools');await toggleDisclosure(ui.c,'workspace-records',true);
  const reveal=[];original.parentNode.scrollIntoView=()=>{assert.ok(displayed(original));reveal.push(original);};await ui.open();
  assert.deepEqual(reveal,[original]);assert.equal(ui.selected(),key('B'));assert.equal(ui.composer(),original);assert.equal(props(elements(original,'textarea')[0]).value,'Edited daily-workspace message');assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));ui.assertIndependent();
  await ui.press('Send',original);assert.match(original.textContent,/Sending; waiting/);const pendingCalls=ui.calls.length;
  for(const panel of panels){await toggleDisclosure(ui.c,panel.getAttribute('id'),true);await toggleDisclosure(ui.c,panel.getAttribute('id'),false);}
  assert.equal(ui.calls.length,pendingCalls);assert.equal(ui.composer(),original);assert.match(original.textContent,/Sending; waiting/);
  await React.act(async()=>send.resolve({threadId:'D'}));assert.equal(ui.composer(),original);assert.match(original.textContent,/Sent to conversation D/);assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));assert.equal(props(name).value,'Unsent local name');ui.assertIndependent();
 });
});

for(const state of ['absent','ready'])test(`first use with Codex ${state} exposes choices and a real access/start route without supplier calls`,async()=>{
 await mounted({initialize:false,beforeMount:account=>{account.state=state;account.generation=state==='absent'?null:g;account.workflowRoot.context.generation=account.generation;account.threads=[];}},async ui=>{
  const start=byId(ui.c,'workspace-start');assert.ok(displayed(start));for(const label of ['Model ','Configured Codex provider '])assert.ok(displayed(labelled(start,'input',label)));assert.ok(displayed(labelled(start,'select','Access entry ')));assert.ok(displayed(button(start,'Start thread')));
  const connection=byId(ui.c,'workspace-connection');if(state==='absent'){assert.equal(disclosureOpen(connection),true,'connection setup is exposed before Codex is ready');assert.ok(displayed(button(ui.c,'Start Codex')));}
  const before=ui.calls.length;await toggleDisclosure(ui.c,'workspace-connection',false);assert.equal(disclosureOpen(connection),false);await followWorkspaceLink(ui.c,'Set up access or start Codex');assert.equal(disclosureOpen(connection),true);assert.ok(displayed(button(ui.c,'Start Codex')));assert.equal(ui.calls.length,before,'setup navigation never starts a supplier');
 });
});

test('file-act anchors reveal the same mounted secondary panel with no command or source selection',async()=>{
 await mounted({},async ui=>{
  const panel=byId(ui.c,'file-acts');assert.ok(panel);const disclosure=byId(ui.c,'workspace-files');assert.equal(disclosureOpen(disclosure),false);const before=ui.calls.length;
  await followWorkspaceLink(ui.c,'Review a workspace draft file for a separate standing act');assert.equal(disclosureOpen(disclosure),true);assert.equal(byId(ui.c,'file-acts'),panel);assert.equal(ui.calls.length,before);ui.assertIndependent();
 });
});

for(const threadId of ['B',null])test(`waiting ${threadId??'unnamed'} request stays outside collapsed tools and opens its exact original source`,async()=>{
 const waiting={modeHomeClass:'account',generation:g,threadId};
 await mounted({waiting,beforeMount:account=>{
  account.waitingRequests={groups:[{...waiting,count:1}],sources:[{modeHomeClass:'account',state:'ready'}],coverage:'Controlled source fixture'};
  account.serverRequests=[{recordKind:'server-request-entry',generation:g,requestIdentity:'daily-original-question',method:'item/tool/requestUserInput',classification:'known-answerable',originClass:'person-input',nativeParameters:{...(threadId?{threadId,turnId:'original-turn',itemId:'original-item'}:{}),isBlocking:false,questions:[{id:'q',header:'Scope',question:'Which supplied boundary?',isOther:false,isSecret:false,options:[{label:'Only supplied design',description:'Use the original source'}]}]},state:'outstanding',replyWriteResult:'not-attempted',acknowledgmentObservation:{status:'not-observed'}}];
 }},async ui=>{
  for(const panel of byId(ui.c,'workspace-tools').querySelectorAll(e=>e.localName==='details'&&e.getAttribute('class')==='workspace-disclosure'))panel.open=false;
  const indicator=region(ui.c,'Requests waiting for your answer');assert.ok(displayed(indicator));assert.match(byId(ui.c,'other-requests').textContent,/Which supplied boundary/);assert.ok(displayed(byId(ui.c,'other-requests')));assert.ok(displayed(region(ui.c,'Content named by an open native confirmation')));
  const before=ui.calls.length;await ui.press(`account · ${threadId?'conversation '+threadId:'no conversation named'}: 1`);
  assert.deepEqual(ui.calls.slice(before).filter(call=>!['host_status','decision_view'].includes(call.command)),[{command:'open_waiting_requests',args:waiting}],'only the original exact group is opened, with no answer/resume/send');
  assert.equal(ui.selected(),threadId?key(threadId):'');assert.ok(displayed(threadId?conversation(ui.c):byId(ui.c,'other-requests')));assert.equal(props(labelled(ui.c,'select','Workflow chat ')).value,'C');assert.equal(props(labelled(ui.c,'select','Authoring conversation ')).value,key('B'));
 });
});

test('ordinary model choice stays local to its full conversation and never enters a prepared Send-to-D request',async()=>{
 await mounted({send:async(command,args)=>{
  assert.equal(command,'workflow_trial_send');assert.equal(args.threadId,'D');assert.equal(Object.hasOwn(args,'model'),false);return {threadId:'D'};
 }},async ui=>{
  await ui.change(labelled(conversation(ui.c),'input','Optional model identifier for next ordinary text turn '),'ordinary-A-model');
  await ui.choose('B');
  const model=()=>labelled(conversation(ui.c),'input','Optional model identifier for next ordinary text turn ');
  assert.equal(props(model()).value,'');await ui.change(model(),'ordinary-B-model');
  const original=ui.composer();await ui.change(elements(original,'textarea')[0],'Prepared text for D');await ui.change(labelled(original,'select','Send to '),key('D'));
  await ui.press('Send',original);
  assert.equal(props(model()).value,'ordinary-B-model','a prepared send consumes no ordinary choice');
  ui.assertIndependent();
 });
});

test('workspace links reveal and focus existing destinations without changing choices or issuing commands',async()=>{
 await mounted({},async ui=>{
  const connection=byId(ui.c,'workspace-connection');const summary=connection.childNodes.find(n=>n.localName==='summary');
  const focused=[];summary.focus=()=>focused.push(summary);
  await toggleDisclosure(ui.c,'workspace-connection',false);
  const before=ui.calls.length;await followWorkspaceLink(ui.c,'Connection & access');
  assert.equal(disclosureOpen(connection),true);assert.deepEqual(focused,[summary]);
  const target=byId(ui.c,'conversation');target.focus=()=>focused.push(target);
  await followWorkspaceLink(ui.c,'Conversation');assert.equal(focused.at(-1),target);assert.equal(target.getAttribute('tabindex'),'-1');
  assert.equal(ui.calls.length,before);ui.assertIndependent();
 });
});

for (const [state,closed,expected] of [['absent',false,'Codex is not connected'],['starting',false,'Codex is starting'],['ready',false,'Codex is connected'],['ready',true,'Codex is not connected'],['refused',false,'Codex could not stay connected']]) {
 test(`connection overview reports ${state}/${closed} without choosing or starting`,async()=>{
  await mounted({initialize:false,beforeMount:account=>{account.state=state;account.generationClosed=closed;}},async ui=>{
   const status=region(ui.c,'Workspace connection status');assert.ok(status);
   assert.match(status.textContent,new RegExp(expected));
   const before=ui.calls.length;
   const link=elements(status,'a')[0];if(link)await followWorkspaceLink(ui.c,link.textContent);
   assert.equal(ui.calls.length,before);
  });
 });
}
