import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
import {continuationFixture} from './support/continuation-fixture.mjs';

// Same receiving shape as ordinaryContinueCase plus the actual producer fields:
// NativeHistory::continue_query excludes turns; resolutions have a revision;
// HistorySession attaches Host::history_admit_resume's genuine activeAdmission.
// This suite exercises the actual mounted consumer with controlled IPC. It is
// not native producer execution or restoration of cold operational authority.
const g={appSession:'continue-fixture',home:'continue-home',spawnCounter:1};
const key=id=>JSON.stringify([g,id]);
const ref='original-owned-resume-request';
const query={factory_id:1,query_id:3,home:g.home,generation:g,method:'thread/resume',params:{threadId:'stored',excludeTurns:true}};
const metadataQuery={...query,query_id:2,method:'thread/read',params:{threadId:'stored',includeTurns:false}};
const unknown={standing:'unknown',reason:'original request-bound App role/source metadata not supplied; native agentRole does not establish it'};
const thread=id=>({generation:g,threadId:id,appRole:{standing:'app-observed',role:null,supply_ref:`sup:${id}`},roleRelation:{kind:'start'},futureGuidanceNotices:[]});
const native=(id='stored',status='notLoaded')=>({id,cliVersion:'0.160.0',createdAt:1,updatedAt:2,cwd:'/invented',ephemeral:false,modelProvider:'configured',preview:'fixture',projectId:null,sessionId:'native-session',source:'appServer',status:{type:status},turns:[],agentRole:'TASK'});
const resume={thread:{...native('stored','idle'),canAcceptDirectInput:true},model:'reported',modelProvider:'configured',cwd:'/invented',approvalPolicy:'on-request',approvalsReviewer:'user',sandbox:{type:'readOnly'}};
const admitted={generation:g,threadId:'stored',status:{type:'idle'},model:'reported',modelProvider:'configured',nativeResumeObserved:true,resumeRequestRef:ref,appRole:unknown};
const deferred=()=>{let resolve;return {promise:new Promise(yes=>{resolve=yes;}),resolve:v=>resolve(v)};};
const document=installMiniDom();
const React=(await import('react')).default;
const {createRoot}=await import('react-dom/client');
const {App}=loadSrc('App');
const props=e=>e[Object.keys(e).find(k=>k.startsWith('__reactProps$'))];
const elements=(c,tag)=>c.querySelectorAll(e=>e.localName===tag);
const button=(c,label)=>elements(c,'button').find(e=>e.textContent===label);
const labelled=(c,tag,label)=>elements(c,tag).find(e=>e.parentNode.textContent.startsWith(label));
const conversation=c=>c.querySelectorAll(e=>e.getAttribute('id')==='conversation')[0];
const choice={model:'person-choice',modelProvider:'configured',entryId:'local-provider'};
const draft='Existing unsent text é / 家\n';

async function mounted(options,check){
 const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
 const calls=[],unexpected=[],timers=new Map(),actions=new Set();let timer=0,fail=false,resumed=false,active='account',starts=0,homes=0,selects=0,holdObserver=true,metadataReads=0;
 const account={state:'ready',generation:g,threads:[thread('existing'),thread('other')],roleLimits:{account:{roles:[]}},nativeHistory:{state:'history-receiving',home:g.home,generation:g,selectionEpoch:0,threads:[{native:native()},{native:native('stored-other')}],dispatches:[]}};
 const keyHome={state:'ready',generation:{...g,home:'other-home'},threads:[],nativeHistory:{state:'history-receiving',home:'other-home',generation:{...g,home:'other-home'},selectionEpoch:0,selected:null,threads:[],dispatches:[]}};
 const snapshot=()=>structuredClone({...(active==='account'?account:keyHome),homeRouting:{activeModeHomeClass:active,entries:[{modeHomeClass:'account'},{modeHomeClass:'api-key'}]}});
 const oldTimers={setInterval:globalThis.setInterval,clearInterval:globalThis.clearInterval};
 globalThis.setInterval=(fn,ms)=>{const id=++timer;timers.set(id,{fn,ms});return id;};globalThis.clearInterval=id=>timers.delete(id);
 const idle=installIdleNativeWaiting(async(command,args)=>{
  calls.push({command,args});
  if(command==='host_status'){if(fail)throw Error('original Continue view unavailable');const value=snapshot();if(options.view)await options.view(value,resumed,calls);if(resumed&&options.observerGate&&holdObserver){holdObserver=false;await options.observerGate.promise;}return value;}
  if(command==='decision_view'){if(resumed&&options.decisionGate)await options.decisionGate.promise;return {rows:[]};}
  if(command==='native_confirmation_content')return [];
  if(command==='select_home'){active=args.modeHomeClass;return {state:'selected'};}
  if(command==='thread_start'){
   assert.deepEqual(args,{...choice,modeHomeClass:'account',role:null,preselected:false});
   if(options.startError)throw options.startError;
   account.threads.push(thread('new-choice'));return {id:91,startGeneration:g,result:{thread:{id:'new-choice'}}};
  }
  if(command==='history_select'){
   assert.deepEqual(args,{generation:g,selectionEpoch:account.nativeHistory.selectionEpoch,threadId:args.threadId});
   account.nativeHistory={...account.nativeHistory,selectionEpoch:account.nativeHistory.selectionEpoch+1,selected:{threadId:args.threadId,state:'indexed-read-only',resumeEligibilityCurrent:false,appRole:unknown}};return structuredClone(account.nativeHistory);
  }
  if(command==='history_action'){
   assert.deepEqual(args,{generation:g,selectionEpoch:account.nativeHistory.selectionEpoch,action:args.action,cursor:null,direction:'desc',reference:null});
   if(args.action==='metadata'){
    metadataReads++;const readQuery={...metadataQuery,query_id:metadataReads+1};
    account.nativeHistory={...account.nativeHistory,selected:{...account.nativeHistory.selected,metadata:{thread:native(account.nativeHistory.selected.threadId)},streamResolutions:{'thread-state':{query:readQuery,revision:metadataReads,outcome:'native-result-observed'}}},dispatches:[...account.nativeHistory.dispatches,{generation:g,home:g.home,requestRef:`original-metadata-request:${metadataReads}`,localQuery:readQuery,writeResult:'written',outcome:'response-observed-result',sourceCurrent:true}]};return structuredClone(account.nativeHistory);
   }
   assert.equal(args.action,'continue');
   const resumeQuery={...query,query_id:metadataReads+2};
   const dispatch={generation:g,home:g.home,requestRef:ref,requestIdentity:43,localQuery:resumeQuery,writeResult:'written',outcome:'response-observed-result',sourceCurrent:true,activeAdmission:admitted};
   const result={...account.nativeHistory,selected:{...account.nativeHistory.selected,state:'resume-response-observed',resumeEligibilityCurrent:true,metadata:{thread:resume.thread},resume,streamResolutions:{'thread-state':{query:resumeQuery,revision:metadataReads+1,outcome:'native-result-observed'}}},dispatches:[...account.nativeHistory.dispatches,dispatch]};
   if(options.admit!==false){account.nativeHistory=structuredClone(result);account.threads.push(structuredClone(admitted));account.continuationContexts=[continuationFixture({generation:g,threadId:'stored',resumeRequestRef:ref,admissionSelectionEpoch:1,state:'partial'})];}
   resumed=true;if(options.failObserver)fail=true;
   if(options.commandGate)await options.commandGate.promise;
   if(options.commandError)throw options.commandError;
   return options.reply?options.reply(structuredClone(result)):structuredClone(result);
  }
  unexpected.push({command,args});throw Error(`Unexpected original command: ${command}`);
 });
 const track=call=>{if(call?.then){actions.add(call);call.then(()=>actions.delete(call),()=>actions.delete(call));}};
 const selected=()=>props(elements(conversation(c),'select')[0]).value;
 const change=async(e,value)=>React.act(()=>{if(e===labelled(c,'select','Stored conversation '))selects++;track(props(e).onChange({target:{value}}));});
 const press=async label=>React.act(async()=>{const e=button(c,label);assert.ok(e,label);assert.equal(props(e).disabled,false,label);if(label==='Start thread')starts++;if(label==='Use api-key home'||label==='Use account home')homes++;track(props(e).onClick());});
 const poll=async()=>React.act(async()=>{const p=[...timers.values()].find(p=>p.fn.toString().includes('host_status'));assert.ok(p);p.fn();});
 const edit=async values=>{for(const[name,value]of Object.entries(values)){const[tag,label]=name==='model'?['input','Model ']:name==='modelProvider'?['input','Configured Codex provider ']:['select','Access entry '];await change(labelled(c,tag,label),value);}};
 const values=()=>({model:props(labelled(c,'input','Model ')).value,modelProvider:props(labelled(c,'input','Configured Codex provider ')).value,entryId:props(labelled(c,'select','Access entry ')).value});
 const context=()=>conversation(c).querySelectorAll(e=>e.getAttribute('aria-label')==='Prior work in continued conversation')[0];
 try{
  await React.act(async()=>root.render(React.createElement(App)));await change(elements(conversation(c),'select')[0],key('existing'));await change(elements(conversation(c),'textarea')[0],draft);await edit(choice);
  await change(labelled(c,'select','Stored conversation '),'stored');for(let n=0;n<(options.metadataReads??1);n++)await press('Read metadata');assert.equal(selected(),key('existing'));assert.equal(calls.filter(x=>x.command==='history_action'&&x.args.action==='continue').length,0);
  await check({c,calls,account,selected,press,poll,change,edit,values,context,recover:()=>{fail=false;},track,chooser:()=>elements(conversation(c),'select')[0],browser:()=>labelled(c,'select','Stored conversation ')});
  assert.deepEqual(unexpected,[]);assert.equal(calls.filter(x=>x.command==='thread_start').length,starts,'only explicit Start presses');assert.equal(calls.filter(x=>x.command==='select_home').length,homes);assert.equal(calls.filter(x=>x.command==='history_select').length,selects);
  assert.equal(calls.filter(x=>x.command==='history_action'&&x.args.action==='continue').length,1,'one original explicit Continue, never a retry on read');
  assert.equal(props(elements(conversation(c),'textarea')[0]).value,draft,'Continue never clears or replaces the unsent draft');
  assert.ok(calls.every(x=>['host_status','decision_view','native_confirmation_content','history_select','history_action','thread_start','select_home'].includes(x.command)),'no implicit send/resume/context drain/role operation');idle.assertClean(c);
 }finally{
  await React.act(async()=>{options.commandGate?.resolve();options.observerGate?.resolve();options.decisionGate?.resolve();await Promise.allSettled([...actions]);});
  const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);assert.equal(timers.size,0);Object.assign(globalThis,oldTimers);
 }
}

test('matched admitted Continue opens original prior context with cold role unknown and draft/chooser intact',async()=>{
 await mounted({},async ui=>{await ui.press('Continue selected conversation');assert.equal(ui.selected(),key('stored'));assert.ok(ui.context());assert.match(ui.context().textContent,/Prior agent response/);assert.match(conversation(ui.c).textContent,/Role not established/);assert.doesNotMatch(conversation(ui.c).textContent,/Role: TASK/);assert.deepEqual(ui.values(),choice);});
});

test('matched resolution after several thread-state queries uses its exact positive revision',async()=>{
 await mounted({metadataReads:4},async ui=>{await ui.press('Continue selected conversation');assert.equal(ui.account.nativeHistory.selected.streamResolutions['thread-state'].revision,5);assert.equal(ui.selected(),key('stored'));assert.ok(ui.context());});
});
test('confirmed Continue waits for its actual operational row and completes once on a later read',async()=>{
 let holdRow=true;
 await mounted({view:async(value,resumed)=>{if(resumed&&holdRow)value.threads=value.threads.filter(row=>row.threadId!=='stored');}},async ui=>{
  await ui.press('Continue selected conversation');assert.equal(ui.selected(),key('existing'));assert.match(ui.c.textContent,/Continue admission confirmed; waiting/);
  holdRow=false;await ui.poll();assert.equal(ui.selected(),key('stored'));assert.ok(ui.context());
  await ui.change(ui.chooser(),key('existing'));await ui.poll();assert.equal(ui.selected(),key('existing'),'completed navigation is consumed, never reselected by another read');
 });
});
test('confirmed Continue survives observer failure and later read recovery without replay',async()=>{
 await mounted({failObserver:true},async ui=>{await ui.press('Continue selected conversation');assert.equal(ui.selected(),key('existing'));assert.equal(ui.context(),undefined);ui.recover();await ui.poll();assert.equal(ui.selected(),key('stored'));assert.ok(ui.context());await ui.poll();assert.deepEqual(ui.values(),choice);});
});
for(const startError of ['Native start refused before send','Native start remains pending/unknown'])test(`newer ordinary Start intent supersedes Continue after ${startError}`,async()=>{
 const commandGate=deferred();await mounted({commandGate,startError},async ui=>{await ui.press('Continue selected conversation');await ui.press('Start thread');assert.equal(ui.selected(),key('existing'));await React.act(async()=>{commandGate.resolve();});assert.equal(ui.selected(),key('existing'));assert.equal(ui.context(),undefined);assert.deepEqual(ui.values(),choice);await ui.poll();assert.equal(ui.selected(),key('existing'));});
});
for(const aba of [false,true])test(`newer selector choice${aba?' away and back':''} supersedes Continue`,async()=>{
 const commandGate=deferred();await mounted({commandGate},async ui=>{await ui.press('Continue selected conversation');assert.equal(props(ui.chooser()).disabled,false);await ui.change(ui.chooser(),key('other'));if(aba)await ui.change(ui.chooser(),key('existing'));await React.act(async()=>{commandGate.resolve();});assert.equal(ui.selected(),key(aba?'existing':'other'));assert.equal(ui.context(),undefined);assert.deepEqual(ui.values(),choice);});
});
test('newer successful Start and later chooser edits survive a delayed Continue',async()=>{
 const commandGate=deferred();await mounted({commandGate},async ui=>{await ui.press('Continue selected conversation');await ui.press('Start thread');assert.equal(ui.selected(),key('new-choice'));await ui.edit({model:'newer-unsent-choice'});const newer=ui.values();await React.act(async()=>{commandGate.resolve();});assert.equal(ui.selected(),key('new-choice'));assert.deepEqual(ui.values(),newer);});
});
test('stale Continue observer cannot restore the original home over a newer home choice',async()=>{
 const observerGate=deferred();await mounted({observerGate},async ui=>{await ui.press('Continue selected conversation');await ui.press('Use api-key home');await ui.edit({model:'new-key-choice',modelProvider:'configured',entryId:'api-key'});const newer=ui.values();await React.act(async()=>{observerGate.resolve();});assert.match(ui.c.textContent,/Active home class: api-key/);assert.notEqual(ui.selected(),key('stored'));assert.deepEqual(ui.values(),newer);});
});
test('home away-and-back intent cancels Continue despite identical final source/key',async()=>{
 const commandGate=deferred();await mounted({commandGate},async ui=>{await ui.press('Continue selected conversation');await ui.press('Use api-key home');await ui.press('Use account home');await ui.edit(choice);await React.act(async()=>{commandGate.resolve();});assert.equal(ui.selected(),key('existing'));assert.deepEqual(ui.values(),choice);});
});
for(const change of ['closure','generation','epoch','query'])test(`pending Continue is cancelled by original ${change} replacement`,async()=>{
 const commandGate=deferred();await mounted({commandGate},async ui=>{await ui.press('Continue selected conversation');if(change==='closure'){ui.account.state='exited';ui.account.generationClosed=true;}if(change==='generation')ui.account.generation={...g,spawnCounter:2};if(change==='epoch')ui.account.nativeHistory.selectionEpoch=2;if(change==='query')ui.account.nativeHistory.selected.streamResolutions['thread-state']={query:{...query,query_id:4},revision:3,outcome:'native-result-observed'};await ui.poll();await React.act(async()=>{commandGate.resolve();});assert.equal(ui.selected(),key('existing'));assert.equal(ui.context(),undefined);});
});
test('new browser selection cancels pending navigation without retargeting the original prior context',async()=>{
 await mounted({failObserver:true},async ui=>{await ui.press('Continue selected conversation');ui.recover();await ui.change(ui.browser(),'stored-other');await ui.poll();assert.equal(ui.selected(),key('existing'));assert.equal(ui.account.continuationContexts[0].threadId,'stored');assert.equal(ui.account.continuationContexts[0].resumeRequestRef,ref);assert.equal(ui.context(),undefined);});
});
for(const commandError of ['original Continue refused before dispatch','original Continue result unavailable'])test(`unknown/refused result never opens a row later listed by a read: ${commandError}`,async()=>{
 await mounted({commandError,admit:commandError.includes('unavailable')},async ui=>{await ui.press('Continue selected conversation');assert.equal(ui.selected(),key('existing'));await ui.poll();assert.equal(ui.selected(),key('existing'));assert.equal(ui.context(),undefined);assert.deepEqual(ui.values(),choice);});
});
const corruptions={
 'missing active admission':r=>{delete r.dispatches.at(-1).activeAdmission;},
 'pending original response':r=>{r.dispatches.at(-1).outcome='pending';},
 'original source unavailable':r=>{r.dispatches.at(-1).sourceCurrent=false;},
 'different original query':r=>{r.dispatches.at(-1).localQuery={...query,query_id:99};},
 'different original receipt':r=>{r.dispatches.at(-1).activeAdmission.resumeRequestRef='another-request';},
 'invalid resolution revision':r=>{r.selected.streamResolutions['thread-state'].revision=0;},
 'superseded original revision':r=>{r.selected.streamResolutions['thread-state'].revision=1;},
 'resume includes unaccepted params':r=>{r.selected.streamResolutions['thread-state'].query.params.excludeTurns=false;r.dispatches.at(-1).localQuery.params.excludeTurns=false;},
};
for(const[name,alter]of Object.entries(corruptions))test(`unmatched returned Continue projection is withheld: ${name}`,async()=>{
 await mounted({reply:r=>{alter(r);return r;}},async ui=>{await ui.press('Continue selected conversation');assert.equal(ui.selected(),key('existing'));await ui.poll();assert.equal(ui.selected(),key('existing'));assert.equal(ui.context(),undefined);});
});
for(const mismatch of ['revision','query','row-ref','row-generation','eligibility'])test(`a current view with wrong ${mismatch} cannot complete original navigation`,async()=>{
 await mounted({view:async(value,resumed)=>{if(!resumed)return;if(mismatch==='revision')value.nativeHistory.selected.streamResolutions['thread-state'].revision=3;if(mismatch==='query')value.nativeHistory.selected.streamResolutions['thread-state'].query={...query,query_id:99};if(mismatch==='eligibility')value.nativeHistory.selected.resumeEligibilityCurrent=false;const row=value.threads.find(t=>t.threadId==='stored');if(mismatch==='row-ref')row.resumeRequestRef='another-request';if(mismatch==='row-generation')row.generation={...g,spawnCounter:2};}},async ui=>{await ui.press('Continue selected conversation');assert.equal(ui.selected(),key('existing'));await ui.poll();assert.equal(ui.selected(),key('existing'));assert.equal(ui.context(),undefined);});
});
test('queued duplicate Continue presses dispatch only the original native request',async()=>{
 const commandGate=deferred();await mounted({commandGate},async ui=>{const click=props(button(ui.c,'Continue selected conversation')).onClick;await React.act(()=>{ui.track(click());ui.track(click());});assert.equal(ui.calls.filter(c=>c.command==='history_action'&&c.args.action==='continue').length,1);await React.act(async()=>{commandGate.resolve();});assert.equal(ui.selected(),key('stored'));});
});
