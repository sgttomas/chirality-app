import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';

// Source-shaped projections from Host::thread_fork_finish and
// HistorySession::reconcile_forks, as exercised by conversation_roles_tests.
// Native admission belongs to that producer, not these renderer fields. This
// suite mounts the actual App and executes no native supplier/window.
const g={appSession:'fork-fixture',home:'account-home',spawnCounter:1};
const kg={...g,home:'key-home'},lgk={...g,home:'local-home'};
const key=(id,generation=g)=>JSON.stringify([generation,id]);
const thread=(id,generation=g,role='WORKING_ITEMS')=>({generation,threadId:id,status:{type:'idle'},model:'fixture-model',modelProvider:'fixture-provider',appRole:{standing:'app-observed',role,supply_ref:`sup:${id}`},roleRelation:{kind:'start'},futureGuidanceNotices:[]});
const forkResult=(generation=g)=>({thread:{...thread('fork-1',generation),forkedFrom:{threadId:'source',forkRequestRef:'original-host-fork-receipt',reportedForkedFromId:'source'},requestedDestination:{source:'inherited from the forked conversation; none chosen at fork'},roleRelation:{kind:'inherited-fork',sourceThread:'source',sourceSupplyRef:'sup:source',forkedFromId:'source'}},role:{kind:'inherited-fork',thread:'fork-1',role:thread('fork-1',generation).appRole},roleSupplyRecord:{state:'not-confirmed'},standing:"Same-role copy: thread/fork carried no instructions, so the fork keeps the source's guidance; the source conversation is unchanged."});
const deferred=()=>{let resolve;return {promise:new Promise(yes=>{resolve=yes;}),resolve:v=>resolve(v)};};
const document=installMiniDom();
const React=(await import('react')).default;
const {createRoot}=await import('react-dom/client');
const {App}=loadSrc('App');
const props=e=>e[Object.keys(e).find(k=>k.startsWith('__reactProps$'))];
const elements=(c,tag)=>c.querySelectorAll(e=>e.localName===tag);
const button=(c,label)=>elements(c,'button').find(e=>e.textContent===label);
const conversation=c=>c.querySelectorAll(e=>e.getAttribute('id')==='conversation')[0];
const labelled=(c,tag,label)=>elements(c,tag).find(e=>e.parentNode.textContent.startsWith(label));
const draft='Unsent composer text é / 家\n';
const choice={model:'person-choice',modelProvider:'fixture-provider',entryId:'local-provider'};

async function mounted(options,check) {
 const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
 const calls=[],unexpected=[],intervals=new Map();const initial=options.initial??'account';let timer=0,active=initial,statusFailure=false,explicitStarts=0,explicitHomes=0;
 const homes={account:{generation:g,threads:[thread('source'),thread('other')],state:'ready'},'api-key':{generation:kg,threads:[thread('source',kg),thread('other',kg)],state:'ready'},'local-provider':{generation:lgk,threads:[thread('source',lgk),thread('other',lgk)],state:'ready'}};
 const snapshot=()=>structuredClone({...homes[active],homeRouting:{activeModeHomeClass:active,entries:[{modeHomeClass:'account'},{modeHomeClass:'api-key'},...(initial==='local-provider'?[{modeHomeClass:'local-provider',generation:lgk,state:'ready'}]:[])]},roleLimits:{account:{roles:[]}}});
 const oldTimers={setInterval:globalThis.setInterval,clearInterval:globalThis.clearInterval};
 globalThis.setInterval=(fn,ms)=>{const id=++timer;intervals.set(id,{fn,ms});return id;};globalThis.clearInterval=id=>intervals.delete(id);
 const idle=installIdleNativeWaiting(async(command,args)=>{
  calls.push({command,args});
  if(command==='host_status'){const value=snapshot();if(statusFailure)throw Error('controlled observer refresh unavailable');if(options.read)await options.read(value,calls);return value;}
  if(command==='decision_view')return {rows:[]};if(command==='native_confirmation_content')return [];
  if(command==='conversation_fork'){
   const origin=homes[initial].generation;assert.deepEqual(args,{generation:origin,threadId:'source'});const result=forkResult(origin);
   if(options.admit!==false)homes[initial].threads.push(structuredClone(result.thread));
   if(options.refreshFails)statusFailure=true;return options.fork?options.fork(result):result;
  }
  if(command==='thread_start'){
   assert.deepEqual(args,{...choice,modeHomeClass:'account',generation:g,role:null,preselected:false});
   if(options.start)return options.start(args);const row=thread('new-choice',g,args.role);homes.account.threads.push(row);
   return {id:91,startGeneration:g,result:{thread:{id:row.threadId},model:'fixture-model',modelProvider:'fixture-provider'},roleSupplyRecord:{state:'not-confirmed'}};
  }
  if(command==='select_home'){if(options.home)await options.home(args);active=args.modeHomeClass;return {state:'selected'};}
  unexpected.push({command,args});throw Error(`Unexpected original command: ${command}`);
 });
 const selected=()=>props(elements(conversation(c),'select')[0]).value;
 const change=async(e,value)=>React.act(()=>props(e).onChange({target:{value}}));
 const edit=async values=>{for(const [name,value]of Object.entries(values)){const [tag,label]=name==='model'?['input','Model ']:name==='modelProvider'?['input','Configured Codex provider ']:['select','Access entry '];await change(labelled(c,tag,label),value);}};
 const values=()=>({model:props(labelled(c,'input','Model ')).value,modelProvider:props(labelled(c,'input','Configured Codex provider ')).value,entryId:props(labelled(c,'select','Access entry ')).value});
 const press=async label=>React.act(async()=>{const b=button(c,label);assert.ok(b,label);assert.equal(props(b).disabled,false,label);if(label==='Start thread')explicitStarts++;if(label==='Use account home')explicitHomes++;props(b).onClick();});
 const poll=async()=>React.act(async()=>{const p=[...intervals.values()].find(p=>p.fn.toString().includes('host_status'));assert.ok(p);p.fn();});
 try{
  await React.act(async()=>root.render(React.createElement(App)));
  await change(elements(conversation(c),'select')[0],key('source',homes[initial].generation));
  // A retained legacy home offers no new-conversation access entry.
  await change(elements(conversation(c),'textarea')[0],draft);await edit(initial==='account'?choice:{model:choice.model,modelProvider:choice.modelProvider});
  assert.equal(calls.filter(c=>c.command==='conversation_fork').length,0,'mount/selection/edits never fork');
  await check({c,calls,homes,snapshot,selected,values,edit,press,poll,change,chooser:()=>elements(conversation(c),'select')[0],recover:()=>{statusFailure=false;},observeHome:async mode=>{active=mode;await poll();},forkCount:()=>calls.filter(c=>c.command==='conversation_fork').length});
  assert.deepEqual(unexpected,[],'strict dispatcher rejects implicit send/resume/start/answer');
  assert.equal(calls.filter(c=>c.command==='thread_start').length,explicitStarts,'only explicit Start presses dispatch Start');
  assert.equal(calls.filter(c=>c.command==='select_home').length,explicitHomes,'Fork never selects a home');
  assert.equal(props(elements(conversation(c),'textarea')[0]).value,draft,'Fork preserves the unsent composer');
  assert.ok(calls.every(c=>['host_status','decision_view','native_confirmation_content','conversation_fork','thread_start','select_home'].includes(c.command)));idle.assertClean(c);
 }finally{const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);assert.equal(intervals.size,0);Object.assign(globalThis,oldTimers);}
}

test('confirmed fork opens once independently of record publication and preserves draft/chooser',async()=>{
 await mounted({},async ui=>{await ui.press('Fork (same role)');assert.equal(ui.selected(),key('fork-1'));assert.equal(ui.forkCount(),1);assert.deepEqual(ui.values(),choice);assert.match(ui.c.textContent,/Role: WORKING_ITEMS/);await ui.poll();assert.equal(ui.forkCount(),1);});
});
test('confirmed fork survives failed observation and selects on a later read without replay',async()=>{
 await mounted({refreshFails:true},async ui=>{await ui.press('Fork (same role)');assert.equal(ui.selected(),key('source'));assert.equal(ui.forkCount(),1);assert.match(ui.c.textContent,/Fork.*admitted|Fork.*confirmed|conversation_fork:.*fork-1/i);assert.deepEqual(ui.values(),choice);ui.recover();await ui.poll();assert.equal(ui.selected(),key('fork-1'));await ui.poll();assert.equal(ui.forkCount(),1);});
});
test('confirmed result does not synthesize an admitted row when its view is unavailable',async()=>{
 let held=true;await mounted({read:async(value,calls)=>{if(held&&calls.some(c=>c.command==='conversation_fork')){held=false;value.threads=value.threads.filter(t=>t.threadId!=='fork-1');}}},async ui=>{await ui.press('Fork (same role)');assert.equal(ui.selected(),key('source'));await ui.poll();assert.equal(ui.selected(),key('fork-1'));assert.equal(ui.forkCount(),1);});
});
test('a lookalike observed row with another fork receipt cannot complete navigation',async()=>{
 await mounted({read:async(value,calls)=>{if(calls.some(c=>c.command==='conversation_fork')){const row=value.threads.find(t=>t.threadId==='fork-1');if(row)row.forkedFrom.forkRequestRef='another-original-receipt';}}},async ui=>{await ui.press('Fork (same role)');assert.equal(ui.selected(),key('source'));await ui.poll();assert.equal(ui.selected(),key('source'));assert.equal(ui.forkCount(),1);});
});
test('native admission remains usable when original role binding is unknown',async()=>{
 await mounted({fork:async result=>({...result,role:{standing:'unknown',reason:'original source binding unavailable'}}),read:async value=>{const row=value.threads.find(t=>t.threadId==='fork-1');if(row)row.appRole={standing:'unknown',reason:'original source binding unavailable'};}},async ui=>{await ui.press('Fork (same role)');assert.equal(ui.selected(),key('fork-1'));assert.match(ui.c.textContent,/Role not established/);assert.equal(ui.forkCount(),1);});
});
test('delayed fork cannot replace a newer successful ordinary Start',async()=>{
 const held=deferred();await mounted({fork:async r=>{await held.promise;return r;}},async ui=>{await ui.press('Fork (same role)');await ui.press('Start thread');assert.equal(ui.selected(),key('new-choice'));await ui.edit({model:'newer-unsent-choice'});const newer=ui.values();await React.act(async()=>{held.resolve();});assert.equal(ui.selected(),key('new-choice'));assert.deepEqual(ui.values(),newer);assert.equal(ui.forkCount(),1);});
});
for(const reason of ['Native start refused before send','Native start remains pending/unknown'])test(`newer Start intent supersedes Fork even after ${reason}`,async()=>{
 const held=deferred();await mounted({fork:async r=>{await held.promise;return r;},start:async()=>{throw Error(reason);}},async ui=>{await ui.press('Fork (same role)');await ui.press('Start thread');assert.equal(ui.selected(),key('source'));await React.act(async()=>{held.resolve();});assert.equal(ui.selected(),key('source'));assert.deepEqual(ui.values(),choice);await ui.poll();assert.equal(ui.selected(),key('source'));assert.equal(ui.forkCount(),1);});
});
test('newer explicit selector choice remains available and takes precedence',async()=>{
 const held=deferred();await mounted({fork:async r=>{await held.promise;return r;}},async ui=>{await ui.press('Fork (same role)');assert.equal(props(ui.chooser()).disabled,false);await ui.change(ui.chooser(),key('other'));await React.act(async()=>{held.resolve();});assert.equal(ui.selected(),key('other'));assert.deepEqual(ui.values(),choice);assert.equal(ui.forkCount(),1);});
});
// The API-key switch is omitted; a supported account choice from an observed
// retained legacy home expresses home intent while the original Fork is pending.
test('home intent supersedes Fork before the new home finishes opening',async()=>{
 const held=deferred(),home=deferred();await mounted({initial:'api-key',fork:async r=>{await held.promise;return r;},home:async()=>home.promise},async ui=>{await ui.press('Fork (same role)');await ui.press('Use account home');await React.act(async()=>{held.resolve();});assert.notEqual(ui.selected(),key('fork-1',kg));await React.act(async()=>{home.resolve();});assert.match(ui.c.textContent,/Selected home: account\./);assert.notEqual(ui.selected(),key('fork-1',kg));assert.equal(ui.forkCount(),1);});
});
test('leaving and returning to the original home never revives old navigation',async()=>{
 const held=deferred();await mounted({fork:async r=>{await held.promise;return r;}},async ui=>{await ui.press('Fork (same role)');await ui.observeHome('api-key');await ui.press('Use account home');await ui.edit(choice);await React.act(async()=>{held.resolve();});assert.notEqual(ui.selected(),key('fork-1'));assert.deepEqual(ui.values(),choice);assert.equal(ui.forkCount(),1);});
});
test('stale Fork observer reply cannot restore an older home over newer choices',async()=>{
 const observer=deferred();let hold=true;await mounted({initial:'api-key',read:async(_s,calls)=>{if(hold&&calls.some(c=>c.command==='conversation_fork')){hold=false;await observer.promise;}}},async ui=>{await ui.press('Fork (same role)');await ui.press('Use account home');await ui.edit({model:'new-account-choice',modelProvider:'fixture-provider',entryId:'local-provider'});const newer=ui.values();await React.act(async()=>{observer.resolve();});assert.match(ui.c.textContent,/Selected home: account\./);assert.notEqual(ui.selected(),key('fork-1',kg));assert.deepEqual(ui.values(),newer);assert.equal(ui.forkCount(),1);});
});
for(const close of ['closed','replacement'])test(`original admission cannot navigate after source ${close}`,async()=>{
 const held=deferred();await mounted({fork:async r=>{await held.promise;return r;}},async ui=>{await ui.press('Fork (same role)');if(close==='closed'){ui.homes.account.state='exited';ui.homes.account.generationClosed=true;}else{ui.homes.account.generation={...g,spawnCounter:2};ui.homes.account.threads=[thread('source',ui.homes.account.generation),thread('fork-1',ui.homes.account.generation)];}await ui.poll();await React.act(async()=>{held.resolve();});assert.notEqual(ui.selected(),key('fork-1'));assert.equal(ui.forkCount(),1);assert.deepEqual(ui.values(),choice);});
});
for(const reason of ['refused-not-sent: choose a current conversation','Fork remains pending (write written); native receipt retained, no automatic retry'])test(`unconfirmed Fork retains source/draft: ${reason}`,async()=>{
 await mounted({admit:false,fork:async()=>{throw Error(reason);}},async ui=>{await ui.press('Fork (same role)');assert.equal(ui.selected(),key('source'));assert.match(ui.c.textContent,/refused-not-sent|Fork remains pending/);await ui.poll();assert.equal(ui.selected(),key('source'));assert.equal(ui.forkCount(),1);assert.deepEqual(ui.values(),choice);});
});
for(const alter of [r=>undefined,r=>({...r,error:{code:-1}}),r=>({...r,thread:{...r.thread,generation:{...g,spawnCounter:2}}}),r=>({...r,thread:{...r.thread,threadId:'source'}}),r=>({...r,thread:{...r.thread,forkedFrom:{...r.thread.forkedFrom,reportedForkedFromId:'unrelated'}}}),r=>({...r,thread:{...r.thread,forkedFrom:{...r.thread.forkedFrom,forkRequestRef:''}}})])test('incomplete/contradictory IPC result cannot choose a conversation merely listed by a read',async()=>{
 await mounted({fork:async r=>alter(r)},async ui=>{await ui.press('Fork (same role)');assert.equal(ui.selected(),key('source'));await ui.poll();assert.equal(ui.selected(),key('source'));assert.equal(ui.forkCount(),1);assert.deepEqual(ui.values(),choice);});
});
test('queued duplicate presses dispatch the original Fork only once',async()=>{
 const held=deferred();await mounted({fork:async r=>{await held.promise;return r;}},async ui=>{const click=props(button(ui.c,'Fork (same role)')).onClick;await React.act(()=>{click();click();});assert.equal(ui.forkCount(),1);await React.act(async()=>{held.resolve();});assert.equal(ui.selected(),key('fork-1'));assert.equal(ui.forkCount(),1);});
});

// Local-home Fork depends on native PR198 eacb1bf651d60884bbc042377865b4359930100d
// (effective-configuration admission at dispatch, write and finish). The
// positive cases run while LOCAL_FORK_AVAILABLE is enabled for that dependency;
// the unavailable case runs only if it is disabled again.
const {LOCAL_FORK_AVAILABLE}=loadSrc('LocalProviderAccess');
const localFork={skip:LOCAL_FORK_AVAILABLE?false:'local Fork awaits native effective-config admission'};
test('local-home Fork is shown unavailable and a retained press dispatches nothing',{skip:LOCAL_FORK_AVAILABLE},async()=>{
 await mounted({initial:'local-provider'},async ui=>{const b=button(ui.c,'Fork (same role)');assert.equal(props(b).disabled,true);assert.match(ui.c.textContent,/Fork isn't available in the local oMLX home yet/);await React.act(async()=>{props(b).onClick();});assert.equal(ui.forkCount(),0);assert.equal(ui.selected(),key('source',lgk));});
});
test('local-home Fork opens once under the original local generation and preserves draft/chooser',localFork,async()=>{
 await mounted({initial:'local-provider'},async ui=>{await ui.press('Fork (same role)');assert.equal(ui.selected(),key('fork-1',lgk));assert.equal(ui.forkCount(),1);await ui.poll();assert.equal(ui.forkCount(),1);});
});
test('account intent from the local home supersedes a pending local Fork',localFork,async()=>{
 const held=deferred(),home=deferred();await mounted({initial:'local-provider',fork:async r=>{await held.promise;return r;},home:async()=>home.promise},async ui=>{await ui.press('Fork (same role)');await ui.press('Use account home');await React.act(async()=>{held.resolve();});assert.notEqual(ui.selected(),key('fork-1',lgk));await React.act(async()=>{home.resolve();});assert.match(ui.c.textContent,/Selected home: account\./);assert.notEqual(ui.selected(),key('fork-1',lgk));assert.equal(ui.forkCount(),1);});
});
test('a replaced local generation cannot receive the original local Fork navigation',localFork,async()=>{
 const held=deferred();await mounted({initial:'local-provider',fork:async r=>{await held.promise;return r;}},async ui=>{await ui.press('Fork (same role)');const next={...lgk,spawnCounter:2};ui.homes['local-provider'].generation=next;ui.homes['local-provider'].threads=[thread('source',next),thread('fork-1',next)];await ui.poll();await React.act(async()=>{held.resolve();});assert.notEqual(ui.selected(),key('fork-1',lgk));assert.notEqual(ui.selected(),key('fork-1',next));assert.equal(ui.forkCount(),1);});
});

// A fork or start refused at its configuration reading: the host returns that sentence alone
// (desktop_startup::access_provider_start_fork_and_key_entry_refusals_…), as Tauri rejects, a string.
const {READING_GATE,READING_WITHDRAWN}=loadSrc('readingSentences');
for(const sentence of [READING_GATE,READING_WITHDRAWN])test(`a Fork refused at its reading shows that sentence alone and keeps source/draft: ${sentence.slice(0,40)}`,async()=>{
 await mounted({admit:false,fork:async()=>{throw sentence;}},async ui=>{await ui.press('Fork (same role)');assert.ok(ui.c.textContent.includes(sentence),'the sentence is shown');assert.doesNotMatch(ui.c.textContent,/Fork outcome is not confirmed|role supply observation/);assert.equal(ui.selected(),key('source'));assert.equal(ui.forkCount(),1);assert.deepEqual(ui.values(),choice);});
});
for(const sentence of [READING_GATE,READING_WITHDRAWN])test(`a Start refused at its reading shows that sentence: ${sentence.slice(0,40)}`,async()=>{
 await mounted({start:async()=>{throw sentence;}},async ui=>{await ui.press('Start thread');assert.ok(ui.c.textContent.includes(`thread_start: ${sentence}`),'the sentence is shown');assert.doesNotMatch(ui.c.textContent,/role supply observation/);assert.deepEqual(ui.values(),choice);});
});
