import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

const document=installMiniDom();
const React=(await import('react')).default;
const {createRoot}=await import('react-dom/client');
const {App}=loadSrc('App');
const props=node=>node[Object.keys(node).find(key=>key.startsWith('__reactProps$'))];
const deferred=()=>{let resolve,reject;const promise=new Promise((yes,no)=>{resolve=yes;reject=no;});return {promise,resolve,reject};};
let cached;
function producer(){
  if(cached)return cached;
  let output;
  if(process.env.CHIRALITY_WAITING_REQUESTS_DTO_LOG)output=readFileSync(process.env.CHIRALITY_WAITING_REQUESTS_DTO_LOG,'utf8');
  else{
    const result=spawnSync('cargo',['test','--offline','--locked','--lib','waiting_requests_tests::','--','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:8*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message??result.stderr+result.stdout);output=result.stdout;
  }
  assert.match(output,/test result: ok\. [1-9]\d* passed; 0 failed;/);
  const read=marker=>{const rows=output.split('\n').filter(line=>line.includes(marker));assert.equal(rows.length,1,marker);return JSON.parse(rows[0].slice(rows[0].indexOf(marker)+marker.length));};
  const dto=read('WAITING_REQUESTS_DTO:');
  assert.ok(dto.native?.intents.account,'actual Host → production menu projection → dispatch → claim fixture');
  return cached={dto,special:read('WAITING_NATIVE_SPECIAL_DTO:'),refusals:read('WAITING_NATIVE_REFUSALS_DTO:')};
}

async function mounted(check,{initial='api-key',pending,claimWait,navigationWait,listenerWait,listenerFailure=false,special=false,loseClaimResponses=0,abandonFailures=0,initialStatusWait}={}){
  const evidence=producer(),dto=special?evidence.special:evidence.dto;
  const container=document.createElement('div');document.body.appendChild(container);let root=createRoot(container);
  const previous=window.__TAURI_INTERNALS__,priorEvents=window.__TAURI_EVENT_PLUGIN_INTERNALS__,priorGet=document.getElementById;
  const calls=[],scrolls=[],handlers=new Map();let active=initial,nextClaim=pending?{...pending,checkpoint:null}:null,nextHandler=0,owned=null,checkpoint=null;
  document.getElementById=id=>{const element=container.querySelectorAll(n=>n.getAttribute('id')===id)[0];if(element)element.scrollIntoView=()=>scrolls.push(id);return element;};
  window.__TAURI_EVENT_PLUGIN_INTERNALS__={unregisterListener(_event,id){handlers.delete(id);}};
  window.__TAURI_INTERNALS__={transformCallback:handler=>{const id=++nextHandler;handlers.set(id,handler);return id;},invoke:async(command,args)=>{
    calls.push({command,args});
    if(command==='host_status'){if(initialStatusWait)await initialStatusWait.promise;return dto[active];}
    if(command==='decision_view')return {rows:[]};
    if(command==='native_confirmation_content')return [];
    if(command==='host_observe')return {sourceUnavailable:true,frames:[]};
    if(command==='plugin:event|listen'){assert.equal(args.event,'chirality-native-waiting');assert.deepEqual(args.target,{kind:'AnyLabel',label:'main'});if(listenerFailure)throw Error('Synthetic listener failure');if(listenerWait)await listenerWait.promise;return args.handler;}
    if(command==='plugin:event|unlisten')return;
    if(command==='checkpoint_native_waiting_ui'){
      const firstAttachment=checkpoint===null;
      checkpoint={consumer:args.consumer,revision:args.revision};
      if(firstAttachment&&args.revision===0&&nextClaim?.target&&nextClaim.checkpoint===null)nextClaim={...nextClaim,checkpoint:{...checkpoint}};
      return;
    }
    if(command==='claim_native_waiting_intent'){
      if(owned?.consumer===args.consumer)return null;
      if(!nextClaim)return null;
      const claim=nextClaim;nextClaim=null;
      if(claim.target)owned={consumer:args.consumer,intentId:claim.intentId};
      if(loseClaimResponses>0&&claim.target){loseClaimResponses--;throw Error('Synthetic claim response lost after host execution');}
      if(claimWait)await claimWait.promise;
      return claim;
    }
    if(command==='finish_native_waiting_intent'){
      if(args.intentId===null&&abandonFailures>0){abandonFailures--;throw Error('Synthetic abandon transport unavailable');}
      if(owned?.consumer===args.consumer&&(args.intentId===null||args.intentId===owned.intentId))owned=null;
      return;
    }
    if(command==='open_waiting_requests'){
      const expected=special?dto.claim.target:Object.values(dto.native.intents).map(c=>c.target).find(t=>t.modeHomeClass===args.modeHomeClass&&t.threadId===args.threadId);
      assert.deepEqual(args,{modeHomeClass:expected.modeHomeClass,generation:expected.generation,threadId:expected.threadId},'exact native target reaches the existing host command');
      if(navigationWait)await navigationWait.promise;
      const result=special?dto.opened:dto.navigation[args.threadId===null?'unnamed':args.modeHomeClass];
      active=result.modeHomeClass;return result;
    }
    throw Error(`Unexpected command ${command}`);
  }};
  const settle=async()=>React.act(async()=>{for(let i=0;i<10;i++)await Promise.resolve();});
  const find=(tag,text)=>container.querySelectorAll(n=>n.localName===tag&&n.textContent===text)[0];
  const conversation=()=>container.querySelectorAll(n=>n.getAttribute('id')==='conversation')[0];
  const select=()=>conversation().querySelectorAll(n=>n.localName==='select')[0];
  const draft=()=>conversation().querySelectorAll(n=>n.localName==='textarea')[0];
  const field=(tag,label)=>container.querySelectorAll(n=>n.localName===tag).find(n=>n.parentNode.textContent.startsWith(label));
  const change=async(element,value)=>{assert.equal(!!props(element).disabled,false);await React.act(()=>props(element).onChange({target:{value}}));};
  const queue=claim=>{assert.ok(!owned&&!nextClaim,'host admits another menu item only after the previous delivery is retired');nextClaim=claim?.target?{...claim,checkpoint:checkpoint?{...checkpoint}:null}:claim;};
  const wake=async claim=>{queue(claim);await React.act(async()=>{for(const [id,handler] of handlers)handler({id,event:'chirality-native-waiting',payload:null});});};
  const press=async text=>{const button=find('button',text);assert.ok(button,text);assert.equal(!!props(button).disabled,false);await React.act(async()=>{props(button).onClick();});};
  try{
    await React.act(async()=>root.render(React.createElement(App)));
    await check({evidence,dto,container,calls,scrolls,select,draft,field,change,press,wake,settle,queue,pending:()=>!!owned||!!nextClaim,
      poll:async()=>React.act(async()=>{await new Promise(resolve=>setTimeout(resolve,1050));}),
      remount:async claim=>{await React.act(()=>root.unmount());owned=null;nextClaim=claim;root=createRoot(container);await React.act(async()=>root.render(React.createElement(App)));},
      unmount:async()=>{await React.act(()=>root.unmount());},
    });
    const allowed=['host_status','decision_view','native_confirmation_content','host_observe','plugin:event|listen','plugin:event|unlisten','claim_native_waiting_intent','finish_native_waiting_intent','checkpoint_native_waiting_ui','open_waiting_requests'];
    assert.deepEqual(calls.filter(c=>!allowed.includes(c.command)),[],'no native response, workflow, resume, start or send command');
  }finally{claimWait?.resolve();navigationWait?.resolve();listenerWait?.resolve();initialStatusWait?.resolve();await settle();await React.act(()=>root.unmount());document.body.removeChild(container);window.__TAURI_INTERNALS__=previous;window.__TAURI_EVENT_PLUGIN_INTERNALS__=priorEvents;document.getElementById=priorGet;}
}

test('a native waiting selection queued before the listener opens its original conversation in mounted App',async()=>{
  const {dto}=producer();
  await mounted(async ui=>{
    const opens=ui.calls.filter(c=>c.command==='open_waiting_requests');
    assert.equal(opens.length,1,'the outside-window selection must reach the actual App navigation consumer');
    assert.equal(props(ui.select()).value,JSON.stringify([dto.account.generation,'shared-thread']));
    assert.deepEqual(ui.scrolls,['conversation']);
    assert.ok(ui.container.textContent.includes('Private synthetic question content'));
    assert.equal(ui.calls.filter(c=>c.command==='finish_native_waiting_intent').length,1);
  },{pending:dto.native.intents.account});
});

test('native wake-up after startup preserves same-home chooser and unsent draft and consumes the claim once',async()=>{
  await mounted(async ui=>{
    await ui.change(ui.field('input','Model '),'separate-unsent-model');
    await ui.change(ui.field('input','Configured Codex provider '),'openai');
    await ui.change(ui.field('select','Access entry '),'api-key');
    await ui.change(ui.draft(),'Unsent / 家 & literal');
    await ui.wake(ui.dto.native.intents['api-key']);
    await ui.wake(null);
    assert.equal(props(ui.select()).value,JSON.stringify([ui.dto['api-key'].generation,'shared-thread']));
    assert.equal(props(ui.field('input','Model ')).value,'separate-unsent-model');
    assert.equal(props(ui.draft()).value,'Unsent / 家 & literal');
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1);
    assert.deepEqual(ui.scrolls,['conversation']);
  });
});

test('native unnamed selection shows only the original home request section',async()=>{
  await mounted(async ui=>{
    await ui.wake(ui.dto.native.intents.unnamed);
    assert.equal(props(ui.select()).value,'');assert.deepEqual(ui.scrolls,['other-requests']);
    assert.match(ui.container.textContent,/Active home class: account/);
  });
});

test('an unloaded literal native identity reaches the host unchanged and opens its original home requests',async()=>{
  const {special}=producer();
  await mounted(async ui=>{
    assert.equal(props(ui.select()).value,'');assert.deepEqual(ui.scrolls,['other-requests']);
    assert.equal(ui.calls.find(c=>c.command==='open_waiting_requests').args.threadId,'R&D && <literal> / 家 "quoted"');
  },{special:true,pending:special.claim});
});

test('listener failure still drains the process-owned startup selection',async()=>{
  const {dto}=producer();
  await mounted(async ui=>{
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1);
    assert.equal(props(ui.select()).value,JSON.stringify([dto.account.generation,'shared-thread']));
  },{pending:dto.native.intents.account,listenerFailure:true});
});

test('native selection while existing home navigation is busy reports refusal instead of silently dropping or retrying it',async()=>{
  const wait=deferred();
  await mounted(async ui=>{
    await ui.press('account · conversation shared-thread: 2');
    await ui.wake(ui.dto.native.intents['api-key']);
    assert.match(ui.container.textContent,/navigation refused while another home or conversation operation is pending/);
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1);
    assert.equal(ui.calls.filter(c=>c.command==='finish_native_waiting_intent').length,1);
    wait.resolve();await ui.settle();
    assert.equal(props(ui.select()).value,JSON.stringify([ui.dto.account.generation,'shared-thread']));
  },{navigationWait:wait});
});

for(const kind of ['conversation','chooser'])test(`a newer ${kind} choice during native claim takes precedence`,async()=>{
  const wait=deferred();
  await mounted(async ui=>{
    await ui.wake(ui.dto.native.intents.account);
    if(kind==='conversation')await ui.change(ui.select(),JSON.stringify([ui.dto['api-key'].generation,'shared-thread']));
    else await ui.change(ui.field('input','Model '),'newer-unsent-model');
    wait.resolve();await ui.settle();
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,0);
    assert.match(ui.container.textContent,/older or uncertain UI checkpoint/);
    assert.deepEqual(ui.scrolls,[]);
    if(kind==='chooser')assert.equal(props(ui.field('input','Model ')).value,'newer-unsent-model');
  },{claimWait:wait});
});

test('newer UI edits during admitted native navigation survive the delayed open result',async()=>{
  const wait=deferred();
  await mounted(async ui=>{
    await ui.wake(ui.dto.native.intents['api-key']);
    await ui.change(ui.select(),'');
    await ui.change(ui.field('input','Model '),'newer-chooser');
    await ui.change(ui.draft(),'Newer unsent draft');
    wait.resolve();await ui.settle();
    assert.equal(props(ui.select()).value,'');assert.deepEqual(ui.scrolls,[]);
    assert.equal(props(ui.field('input','Model ')).value,'newer-chooser');
    assert.equal(props(ui.draft()).value,'Newer unsent draft');
    assert.match(ui.container.textContent,/navigation superseded/);
  },{navigationWait:wait});
});

for(const kind of ['reload','closure'])test(`actual host ${kind} refusal is displayed without any navigation fallback`,async()=>{
  const {refusals}=producer();
  await mounted(async ui=>{
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,0);
    assert.ok(ui.container.textContent.includes(refusals[kind].refused));
    assert.deepEqual(ui.scrolls,[]);
  },{pending:refusals[kind]});
});

test('reload during claim never opens a consumed target and cleans up the old listener',async()=>{
  const wait=deferred();
  await mounted(async ui=>{
    await ui.wake(ui.dto.native.intents.account);
    await ui.unmount();
    wait.resolve();await ui.settle();
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,0);
    assert.equal(ui.calls.filter(c=>c.command==='plugin:event|unlisten').length,1);
    await ui.remount(ui.evidence.refusals.reload);
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,0);
    assert.match(ui.container.textContent,/interrupted by a window reload/);
  },{claimWait:wait});
});

test('uncertain claim IPC reports failure and abandons only its consumer rather than retrying navigation',async()=>{
  const wait=deferred();
  await mounted(async ui=>{
    await ui.wake(ui.dto.native.intents.account);
    wait.reject(Error('Synthetic lost claim response'));await ui.settle();
    assert.match(ui.container.textContent,/Synthetic lost claim response/);
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,0);
    const abandon=ui.calls.find(c=>c.command==='finish_native_waiting_intent');
    assert.equal(abandon.args.intentId,null);
    assert.equal(abandon.args.consumer,ui.calls.filter(c=>c.command==='claim_native_waiting_intent').at(-1).args.consumer);
  },{claimWait:wait});
});


test('a newer chooser edit during initial listener installation supersedes the queued native selection',async()=>{
  const wait=deferred();const {dto}=producer();
  await mounted(async ui=>{
    await ui.change(ui.field('input','Model '),'newer-during-listen');
    wait.resolve();await ui.settle();
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,0);
    assert.match(ui.container.textContent,/older or uncertain UI checkpoint/);
    assert.equal(props(ui.field('input','Model ')).value,'newer-during-listen');
  },{pending:dto.native.intents.account,listenerWait:wait});
});


test('lost native wake followed by a newer conversation choice refuses the queued older target',async()=>{
  await mounted(async ui=>{
    ui.queue(ui.dto.native.intents.account); // Native selection occurred; its wake was lost.
    const newer=JSON.stringify([ui.dto['api-key'].generation,'shared-thread']);
    await ui.change(ui.select(),newer);
    await ui.poll();
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,0,
      'recovery must bind to UI at native selection, not UI when the poll starts');
    assert.equal(props(ui.select()).value,newer);assert.deepEqual(ui.scrolls,[]);
    assert.match(ui.container.textContent,/older|uncertain|superseded/);
  });
});

test('lost native wake with unchanged UI recovers its original target exactly once',async()=>{
  await mounted(async ui=>{
    ui.queue(ui.dto.native.intents.account);
    await ui.poll();await ui.poll();
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1);
    assert.equal(props(ui.select()).value,JSON.stringify([ui.dto.account.generation,'shared-thread']));
  });
});

test('a new native click after current UI checkpoint acknowledgment opens its own target',async()=>{
  await mounted(async ui=>{
    await ui.change(ui.select(),JSON.stringify([ui.dto['api-key'].generation,'shared-thread']));
    await ui.settle(); // Allow the current UI checkpoint handshake to complete.
    await ui.wake(ui.dto.native.intents.account);
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1);
    assert.equal(props(ui.select()).value,JSON.stringify([ui.dto.account.generation,'shared-thread']));
  });
});

test('lost claim response and failed abandon retry cleanup before admitting another menu selection',async()=>{
  await mounted(async ui=>{
    await ui.wake(ui.dto.native.intents.account);
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,0);
    assert.equal(ui.pending(),true,'host still owns the uncertain claim after the first abandon failed');
    await ui.poll();
    assert.equal(ui.pending(),false,'recovery retries abandonment until the host acknowledges it');
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,0,'cleanup cannot replay uncertain navigation');
    await ui.wake(ui.dto.native.intents['api-key']);
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1,'a later explicit native selection is usable again');
    assert.equal(props(ui.select()).value,JSON.stringify([ui.dto['api-key'].generation,'shared-thread']));
  },{loseClaimResponses:1,abandonFailures:1});
});


test('a chooser edit before the first host snapshot refuses an older unbound startup selection',async()=>{
  const wait=deferred();const {dto}=producer();
  await mounted(async ui=>{
    await ui.change(ui.field('input','Model '),'newer-before-first-attachment');
    wait.resolve();await ui.settle();
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,0,
      'first attachment cannot label a prior native selection as newer than an already edited UI');
    // The first host snapshot independently binds the chooser to its actual
    // home. Native waiting must preserve that source guard and refuse this
    // older selection, rather than assigning it the edited UI's checkpoint.
    assert.match(ui.container.textContent,/older or uncertain UI checkpoint/);
    await ui.wake(ui.dto.native.intents.account);
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1,
      'a fresh click after the first acknowledgment remains usable');
  },{pending:dto.native.intents.account,initialStatusWait:wait});
});


test('first native click after an acknowledged chooser edit succeeds while listener installation was delayed',async()=>{
  const wait=deferred();
  await mounted(async ui=>{
    await ui.change(ui.field('input','Model '),'newer-before-first-listen');
    await ui.settle();
    const acknowledged=ui.calls.filter(c=>c.command==='checkpoint_native_waiting_ui').at(-1);
    assert.ok(acknowledged.args.revision>0,'the edited UI checkpoint is acknowledged before the native selection');
    assert.equal(ui.calls.filter(c=>c.command==='claim_native_waiting_intent').length,0,'listener installation has delayed the first pump');
    ui.queue(ui.dto.native.intents.account); // A fresh selection at that acknowledged checkpoint.
    wait.resolve();await ui.settle();
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1,'the first fresh click must open without requiring a second click');
    assert.equal(props(ui.select()).value,JSON.stringify([ui.dto.account.generation,'shared-thread']));
    assert.deepEqual(ui.scrolls,['conversation']);
    assert.equal(ui.calls.filter(c=>c.command==='finish_native_waiting_intent').length,1);
    assert.doesNotMatch(ui.container.textContent,/navigation superseded|older or uncertain UI checkpoint/);
    await ui.wake(null);
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1,'the consumed selection never replays');
  },{listenerWait:wait});
});
