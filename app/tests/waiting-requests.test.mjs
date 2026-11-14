import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import './support/rust-prebuild.mjs';

const document=installMiniDom();
const React=(await import('react')).default;
const {createRoot}=await import('react-dom/client');
const {App}=loadSrc('App');
const props=node=>node[Object.keys(node).find(key=>key.startsWith('__reactProps$'))];
const find=(container,tag,text)=>container.querySelectorAll(node=>node.localName===tag&&node.textContent===text)[0];
// The account home's one connection route; the model field and this route exist only in the account home.
const ROUTE='Use my ChatGPT account (built-in OpenAI)';
let cached, stale;
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
  const marker='WAITING_REQUESTS_DTO:';const rows=output.split('\n').filter(line=>line.includes(marker));assert.equal(rows.length,1);
  const staleMarker='WAITING_REQUESTS_STALE_DTO:';const staleRow=output.split('\n').find(line=>line.includes(staleMarker));
  stale=staleRow?JSON.parse(staleRow.slice(staleRow.indexOf(staleMarker)+staleMarker.length)):null;
  return cached=JSON.parse(rows[0].slice(rows[0].indexOf(marker)+marker.length));
}

// The API-key switch is omitted; selection from a retained legacy home uses the account choice.
test('actual two-home Host requests remain visible in the App overview after selecting the other home',async()=>{
  const dto=producer();const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
  let active='api-key';const calls=[];
  const idle=installIdleNativeWaiting(async(command,args)=>{
    calls.push({command,args});if(command==='host_status')return dto[active];if(command==='decision_view')return {rows:[]};if(command==='native_confirmation_content')return [];
    if(command==='host_observe')return {sourceUnavailable:true,error:'Synthetic fixture does not replay observer journal frames',frames:[]};
    if(command==='select_home'){active=args.modeHomeClass;return {state:'selected'};}
    throw Error(`Unexpected command ${command}`);
  });
  const indicator=()=>container.querySelectorAll(node=>node.getAttribute('aria-label')==='Requests waiting for your answer')[0];
  try{
    await React.act(async()=>root.render(React.createElement(App)));
    await React.act(async()=>props(find(container,'button','Use account home')).onClick());
    assert.match(container.textContent,/Selected home: account\./);
    const place=container.querySelectorAll(node=>node.getAttribute('aria-label')==='Waiting on you')[0];
    assert.match(place.querySelectorAll(node=>node.localName==='summary')[0].textContent,/^Waiting on you: 4\+ \(4 requests from Codex; not every source read\)$/,'(this harness reads no returns, so "+") the inactive retained key request is counted alongside the active account requests, in the one count');
    assert.match(indicator().textContent,/Requests from Codex waiting for your answer, by home and conversation/);
    assert.match(indicator().textContent,/account.*shared-thread.*2/);
    assert.match(indicator().textContent,/api-key.*shared-thread.*1/);
    assert.match(indicator().textContent,/no conversation named.*1/);
    assert.deepEqual(calls.filter(call=>!['host_status','decision_view','native_confirmation_content','host_observe','select_home'].includes(call.command)),[],'overview and home choice never answer, resume or send');
  }finally{const renderedText=container.textContent;await React.act(()=>root.unmount());document.body.removeChild(container);idle.restore(renderedText);}
});

const deferred=()=>{let resolve;const promise=new Promise(yes=>{resolve=yes;});return {promise,resolve};};
async function mounted(check,{initial='api-key',navigationWait,decisionWait,wrongRefresh=false,refuse=false,failAfterOpen=false}={}){
  const dto=producer();const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
  let active=initial,opened=false;const calls=[],scrolls=[];const priorGet=document.getElementById;
  document.getElementById=id=>{const element=container.querySelectorAll(node=>node.getAttribute('id')===id)[0];if(element)element.scrollIntoView=()=>scrolls.push(id);return element;};
  const idle=installIdleNativeWaiting(async(command,args)=>{
    calls.push({command,args});
    if(command==='host_status'){if(failAfterOpen&&opened)throw 'INVENTED_PRIVATE_REFRESH_DIAGNOSTIC_92';return dto[wrongRefresh&&opened?'api-key':active];}
    if(command==='decision_view'){if(opened&&decisionWait)await decisionWait.promise;return {rows:[]};}
    if(command==='native_confirmation_content')return [];
    if(command==='host_observe')return {sourceUnavailable:true,error:'Synthetic fixture does not replay observer journal frames',frames:[]};
    assert.equal(command,'open_waiting_requests','navigation is the only command this view may issue');
    const result=dto.navigation[args.threadId===null?'unnamed':args.modeHomeClass];
    assert.deepEqual(args,{modeHomeClass:result.modeHomeClass,generation:result.generation,threadId:result.threadId},'exact original source/group reaches the native boundary');
    if(navigationWait)await navigationWait.promise;
    if(refuse)throw Error(stale.error);
    active=result.modeHomeClass;opened=true;return result;
  });
  const conversation=()=>container.querySelectorAll(node=>node.getAttribute('id')==='conversation')[0];
  const byTag=(c,tag)=>c.querySelectorAll(node=>node.localName===tag);
  const field=(tag,label)=>byTag(container,tag).find(node=>node.parentNode.textContent.startsWith(label));
  const settle=async()=>React.act(async()=>{for(let i=0;i<8;i++)await Promise.resolve();});
  const press=async text=>{const b=find(container,'button',text);assert.ok(b,text);assert.equal(!!props(b).disabled,false,text);await React.act(async()=>{props(b).onClick();});};
  const change=async(element,value)=>{assert.equal(!!props(element).disabled,false,'no edit through disabled controls');await React.act(()=>props(element).onChange({target:{value}}));};
  try{
    await React.act(async()=>root.render(React.createElement(App)));
    const routeChosen=()=>{const b=find(container,'button',ROUTE);return !!b&&props(b)['aria-pressed']===true;};
    const choice=()=>({model:field('input','Model ')?props(field('input','Model ')).value:null,route:routeChosen()});
    await check({dto,container,calls,scrolls,press,change,settle,conversation,field,routeChosen,choice,select:()=>byTag(conversation(),'select')[0],draft:()=>byTag(conversation(),'textarea')[0]});
  }finally{navigationWait?.resolve();decisionWait?.resolve();await settle();const renderedText=container.textContent;await React.act(()=>root.unmount());document.body.removeChild(container);idle.restore(renderedText);document.getElementById=priorGet;}
}

test('an explicit all-home click opens the original full-generation conversation despite a same-ID active-home conversation',async()=>{
  await mounted(async ui=>{
    await ui.change(ui.select(),JSON.stringify([ui.dto['api-key'].generation,'shared-thread']));
    await ui.change(ui.draft(),'Kept unsent draft / 家');
    assert.ok(!ui.container.textContent.includes('Private synthetic question content'),'inactive account question content is absent');
    await ui.press('account · thread shared-thread: 2');
    assert.equal(props(ui.select()).value,JSON.stringify([ui.dto.account.generation,'shared-thread']));
    assert.equal(props(ui.draft()).value,'Kept unsent draft / 家');
    assert.ok(ui.container.textContent.includes('Private synthetic question content'),'ordinary selected-home view receives the original cards');
    assert.deepEqual(ui.scrolls,['conversation']);
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1);
  });
});

test('an unnamed waiting group opens its original home request section without loading or resuming a conversation',async()=>{
  await mounted(async ui=>{
    await ui.change(ui.select(),JSON.stringify([ui.dto['api-key'].generation,'shared-thread']));
    await ui.press('account · no conversation named: 1');
    assert.equal(props(ui.select()).value,'');assert.deepEqual(ui.scrolls,['other-requests']);
    assert.ok(ui.container.textContent.includes('Private synthetic question content'));
  });
});

test('native stale-source refusal never opens a same-ID successor or falls back to the active home',async()=>{
  await mounted(async ui=>{
    const selected=JSON.stringify([ui.dto['api-key'].generation,'shared-thread']);await ui.change(ui.select(),selected);
    await ui.press('account · thread shared-thread: 2');
    assert.equal(props(ui.select()).value,selected);assert.deepEqual(ui.scrolls,[]);
    assert.match(ui.container.textContent,/Original waiting-request source is no longer current/);
  },{refuse:true});
});

test('a mismatched post-navigation source refresh never selects or scrolls to a lookalike conversation',async()=>{
  await mounted(async ui=>{
    const selected=JSON.stringify([ui.dto['api-key'].generation,'shared-thread']);await ui.change(ui.select(),selected);
    await ui.press('account · thread shared-thread: 2');
    assert.equal(props(ui.select()).value,selected);assert.deepEqual(ui.scrolls,[]);assert.match(ui.container.textContent,/navigation superseded/);
  },{wrongRefresh:true});
});

test('a newer conversation choice made during navigation takes precedence over its delayed result',async()=>{
  const wait=deferred();
  await mounted(async ui=>{
    await ui.change(ui.select(),JSON.stringify([ui.dto['api-key'].generation,'shared-thread']));
    await ui.press('account · thread shared-thread: 2');
    assert.equal(props(find(ui.container,'button','account · thread shared-thread: 2')).disabled,true);
    assert.equal(props(find(ui.container,'button','Use account home')).disabled,true,'a manual home choice is not offered while the original navigation is pending');
    assert.equal(find(ui.container,'button','Use api-key home'),undefined,'no API-key home switch is offered');
    assert.equal(ui.calls.filter(c=>c.command==='select_home').length,0,'no manual switch is dispatched during the pending navigation');
    await ui.change(ui.select(),'');wait.resolve();await ui.settle();
    assert.equal(props(ui.select()).value,'');assert.deepEqual(ui.scrolls,[]);assert.match(ui.container.textContent,/navigation superseded/);
  },{navigationWait:wait});
});

test('navigation invalidates the prior-home chooser at intent and preserves newer target-home edits through delayed refresh',async()=>{
  const wait=deferred();
  await mounted(async ui=>{
    // The retained legacy home offers no connection route or model field, so no prior-home choice can be made.
    assert.deepEqual(ui.choice(),{model:null,route:false});
    await ui.press('account · thread shared-thread: 2');
    assert.deepEqual(ui.choice(),{model:'',route:false});
    assert.match(ui.container.textContent,/Selected home: account\./,'target source is rendered while its independent decision refresh waits');
    // While the target home's refresh is pending the route is not offered; the model field can still be edited.
    assert.equal(props(find(ui.container,'button',ROUTE)).disabled,true);
    await ui.change(ui.field('input','Model '),'target-model');
    wait.resolve();await ui.settle();
    assert.deepEqual(ui.choice(),{model:'target-model',route:false});
    await ui.press(ROUTE);assert.deepEqual(ui.choice(),{model:'target-model',route:true});
    assert.equal(ui.calls.filter(c=>c.command==='thread_start').length,0);
  },{decisionWait:wait});
});

test('same-home waiting navigation preserves a separate unconsumed new-conversation choice and draft',async()=>{
  for(const initial of ['account','api-key']) {
    await mounted(async ui=>{
      // Only the account home offers a new-conversation choice; the retained legacy home offers none.
      const kept=initial==='account'?{model:'unsent-new-model',route:true}:{model:null,route:false};
      if(initial==='account'){await ui.press(ROUTE);await ui.change(ui.field('input','Model '),'unsent-new-model');}
      assert.deepEqual(ui.choice(),kept);
      await ui.change(ui.draft(),'Kept unsent draft / 家');
      await ui.press(`${initial} · thread shared-thread: ${initial==='account'?2:1}`);
      assert.deepEqual(ui.choice(),kept);
      assert.equal(props(ui.draft()).value,'Kept unsent draft / 家');
      assert.equal(props(ui.select()).value,JSON.stringify([ui.dto[initial].generation,'shared-thread']));
      assert.deepEqual(ui.scrolls,['conversation']);
      assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1);
    },{initial});
  }
});

// The account home offers no API-key switch. A retained legacy key home offers
// only the account choice and no new conversation, so each home queues the
// presses it actually offers against the shared pending latch.
for(const initial of ['account','api-key'])test(`same-home pending navigation keeps its shared latch and preserves newer chooser, selection and draft edits (${initial})`,async()=>{
  const wait=deferred(),account=initial==='account';
  await mounted(async ui=>{
    await ui.change(ui.select(),JSON.stringify([ui.dto[initial].generation,'shared-thread']));
    if(account){await ui.press(ROUTE);await ui.change(ui.field('input','Model '),'unsent-new-model');}
    const kept=account?{model:'unsent-new-model',route:true}:{model:null,route:false};
    assert.deepEqual(ui.choice(),kept);
    const waiting=`${initial} · thread shared-thread: ${account?2:1}`;
    assert.equal(find(ui.container,'button','Use api-key home'),undefined,'no API-key home switch is offered');
    assert.equal(!!find(ui.container,'button','Use account home'),!account,'the account choice is offered only from a retained legacy home');
    const queuedOpen=props(find(ui.container,'button',waiting)).onClick;
    const queuedHome=account?null:props(find(ui.container,'button','Use account home')).onClick;
    const queuedStart=props(find(ui.container,'button','Start thread')).onClick;
    assert.equal(!!props(find(ui.container,'button','Start thread')).disabled,!account,'a legacy home offers no new conversation');
    await ui.press(waiting);
    assert.deepEqual(ui.choice(),kept);
    for(const text of [waiting,...(account?[]:['Use account home']),'Start thread'])assert.equal(props(find(ui.container,'button',text)).disabled,true,text);
    await React.act(async()=>{queuedOpen();await queuedHome?.();await queuedStart();});
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1,'queued presses share the synchronous pending latch');
    assert.equal(ui.calls.filter(c=>c.command==='select_home'||c.command==='thread_start').length,0);
    if(account)await ui.change(ui.field('input','Model '),'newer-model');
    await ui.change(ui.select(),'');
    await ui.change(ui.draft(),'Newer unsent draft / 家');
    wait.resolve();await ui.settle();
    assert.deepEqual(ui.choice(),account?{model:'newer-model',route:true}:{model:null,route:false});
    assert.equal(props(ui.draft()).value,'Newer unsent draft / 家');
    assert.equal(props(ui.select()).value,'');assert.deepEqual(ui.scrolls,[]);
    assert.match(ui.container.textContent,/navigation superseded/);
    if(!account)assert.equal(props(find(ui.container,'button','Use account home')).disabled,false);
    assert.equal(!!props(find(ui.container,'button','Start thread')).disabled,!account);
    assert.equal(ui.calls.filter(c=>c.command==='select_home'||c.command==='thread_start').length,0);
  },{initial,navigationWait:wait});
});

// Navigation whose command succeeds and whose status refresh then fails: no navigation is claimed
// or made, the line shows the fixed refresh line once, and the raw refresh text is never shown.
test('a waiting-request navigation whose refresh fails shows only the fixed line and navigates nothing',async()=>{
  const {REFRESH_FAILED}=loadSrc('statusRefresh');
  await mounted(async ui=>{
    const before=props(ui.select()).value;
    await ui.press('account · thread shared-thread: 2');await ui.settle();
    assert.ok(ui.container.textContent.includes(REFRESH_FAILED),'the fixed refresh line');
    assert.doesNotMatch(ui.container.textContent,/INVENTED_PRIVATE_REFRESH_DIAGNOSTIC_92|Waiting-request navigation:|superseded or its original source/);
    assert.equal(props(ui.select()).value,before,'nothing is navigated without a status read');
    assert.equal(ui.calls.filter(c=>c.command==='open_waiting_requests').length,1);
  },{failAfterOpen:true});
});
