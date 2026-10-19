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
const key=(id,generation=g)=>JSON.stringify([generation,id]);
const thread=(id,generation=g,role='WORKING_ITEMS')=>({generation,threadId:id,status:{type:'idle'},model:'fixture-model',modelProvider:'fixture-provider',appRole:{standing:'app-observed',role,supply_ref:`sup:${id}`},roleRelation:{kind:'start'},futureGuidanceNotices:[]});
const forkResult=()=>({thread:{...thread('fork-1'),forkedFrom:{threadId:'source',forkRequestRef:'original-host-fork-receipt',reportedForkedFromId:'source'},requestedDestination:{source:'inherited from the forked conversation; none chosen at fork'},roleRelation:{kind:'inherited-fork',sourceThread:'source',sourceSupplyRef:'sup:source',forkedFromId:'source'}},role:{kind:'inherited-fork',thread:'fork-1',role:thread('fork-1').appRole},roleSupplyRecord:{state:'not-confirmed'},standing:"Same-role copy: thread/fork carried no instructions, so the fork keeps the source's guidance; the source conversation is unchanged."});
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
 const calls=[],unexpected=[],intervals=new Map();let timer=0,active='account',statusFailure=false,explicitStarts=0,explicitHomes=0;
 const homes={account:{generation:g,threads:[thread('source'),thread('other')],state:'ready'},'api-key':{generation:{...g,home:'key-home'},threads:[],state:'ready'}};
 const snapshot=()=>structuredClone({...homes[active],homeRouting:{activeModeHomeClass:active,entries:[{modeHomeClass:'account'},{modeHomeClass:'api-key'}]},roleLimits:{account:{roles:[]}}});
 const oldTimers={setInterval:globalThis.setInterval,clearInterval:globalThis.clearInterval};
 globalThis.setInterval=(fn,ms)=>{const id=++timer;intervals.set(id,{fn,ms});return id;};globalThis.clearInterval=id=>intervals.delete(id);
 const idle=installIdleNativeWaiting(async(command,args)=>{
  calls.push({command,args});
  if(command==='host_status'){const value=snapshot();if(statusFailure)throw Error('controlled observer refresh unavailable');if(options.read)await options.read(value,calls);return value;}
  if(command==='decision_view')return {rows:[]};if(command==='native_confirmation_content')return [];
  if(command==='conversation_fork'){
   assert.deepEqual(args,{generation:g,threadId:'source'});const result=forkResult();
   if(options.admit!==false)homes.account.threads.push(structuredClone(result.thread));
   if(options.refreshFails)statusFailure=true;return options.fork?options.fork(result):result;
  }
  if(command==='thread_start'){
   assert.deepEqual(args,{...choice,modeHomeClass:'account',role:null,preselected:false});
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
 const press=async label=>React.act(async()=>{const b=button(c,label);assert.ok(b,label);assert.equal(props(b).disabled,false,label);if(label==='Start thread')explicitStarts++;if(label==='Use account home'||label==='Use api-key home')explicitHomes++;props(b).onClick();});
 const poll=async()=>React.act(async()=>{const p=[...intervals.values()].find(p=>p.fn.toString().includes('host_status'));assert.ok(p);p.fn();});
 try{
  await React.act(async()=>root.render(React.createElement(App)));
  await change(elements(conversation(c),'select')[0],key('source'));
  await change(elements(conversation(c),'textarea')[0],draft);await edit(choice);
  assert.equal(calls.filter(c=>c.command==='conversation_fork').length,0,'mount/selection/edits never fork');
  await check({c,calls,homes,snapshot,selected,values,edit,press,poll,change,chooser:()=>elements(conversation(c),'select')[0],recover:()=>{statusFailure=false;},forkCount:()=>calls.filter(c=>c.command==='conversation_fork').length});
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
test('home intent supersedes Fork before the new home finishes opening',async()=>{
 const held=deferred(),home=deferred();await mounted({fork:async r=>{await held.promise;return r;},home:async()=>home.promise},async ui=>{await ui.press('Fork (same role)');await ui.press('Use api-key home');await React.act(async()=>{held.resolve();});assert.notEqual(ui.selected(),key('fork-1'));await React.act(async()=>{home.resolve();});assert.match(ui.c.textContent,/Active home class: api-key/);assert.equal(ui.forkCount(),1);});
});
test('leaving and returning to the original home never revives old navigation',async()=>{
 const held=deferred();await mounted({fork:async r=>{await held.promise;return r;}},async ui=>{await ui.press('Fork (same role)');await ui.press('Use api-key home');await ui.press('Use account home');await ui.edit(choice);await React.act(async()=>{held.resolve();});assert.notEqual(ui.selected(),key('fork-1'));assert.deepEqual(ui.values(),choice);assert.equal(ui.forkCount(),1);});
});
test('stale Fork observer reply cannot restore an older home over newer choices',async()=>{
 const observer=deferred();let hold=true;await mounted({read:async(_s,calls)=>{if(hold&&calls.some(c=>c.command==='conversation_fork')){hold=false;await observer.promise;}}},async ui=>{await ui.press('Fork (same role)');await ui.press('Use api-key home');await ui.edit({model:'new-key-choice',modelProvider:'openai',entryId:'api-key'});const newer=ui.values();await React.act(async()=>{observer.resolve();});assert.match(ui.c.textContent,/Active home class: api-key/);assert.notEqual(ui.selected(),key('fork-1'));assert.deepEqual(ui.values(),newer);assert.equal(ui.forkCount(),1);});
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
