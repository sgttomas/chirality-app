// Actual private Host/refusal publication -> the maintained visible consumers.
// Invented peer/files only; no supplier/model/human-act qualification.
import {test,after} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,mkdtempSync,rmSync,existsSync,writeFileSync,renameSync} from 'node:fs';
import {execFileSync,spawn} from 'node:child_process';
import {createRequire} from 'node:module';
import {tmpdir} from 'node:os';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {localRequire} from './support/load-src.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
const app=new URL('../',import.meta.url),out=mkdtempSync(`${tmpdir()}/access-provider-private-`);
const document=installMiniDom();
const {createRoot}=await import('react-dom/client');
const {App}=loadSrc('App');
after(()=>rmSync(out,{recursive:true}));
const url=new URL('src/ConversationRoles.tsx',app),compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});
const exports={};new Function('require','exports',compiled.outputText)(localRequire(createRequire(url)),exports);
const h=(c,p)=>renderToStaticMarkup(React.createElement(c,p));
const canary='INVENTED_PRIVATE_PROVIDER_CANARY_481';
test('actual refusal stays safe in current source JSON and quoted role history',()=>{
 execFileSync('cargo',['test','--offline','--locked','--lib','access_provider_actual_private_refusal_output_has_only_safe_public_consumers','--','--test-threads=1'],{cwd:new URL('src-tauri/',app),env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CHIRALITY_TEST_OUTPUT_DIRECTORY:out},stdio:'inherit'});
 const packet=JSON.parse(readFileSync(`${out}/access-provider-private.json`,'utf8'));
 assert.match(packet.refusal,/credential element; no thread\/start sent/);
 assert.equal(packet.roleSupplyRecord.state,'written');assert.ok(packet.quotedRole.observations.length>0);
 const html=h(exports.RoleSupplyHistory,{view:packet.quotedRole})+h(exports.SupplyStatus,{supply:{state:'refused-before-send',reason:packet.refusal,roleSupplyRecord:packet.roleSupplyRecord}});
 assert.match(html,/credential element/);assert.doesNotMatch(html,new RegExp(canary));
 const raw=JSON.stringify({lifecycle:packet.snapshot.lifecycle,clientRequests:packet.snapshot.clientRequests,journal:packet.snapshot.journal,recordedRecovery:packet.recordedRecovery});
 assert.doesNotMatch(raw,new RegExp(canary));assert.match(raw,/private provider configuration outcome projection/);
 assert.equal(packet.snapshot.clientRequests.filter(r=>r.method==='thread/start').length,0);

});
test('shared Start and Continue-as fields explain actual entry/provider refusal and preserve input',()=>{
 const html=h(exports.ModelProviderFields,{model:'chosen-model',modelProvider:'nonloopback-anonymous',setModel:()=>{},setModelProvider:()=>{}});
 assert.match(html,/cloud entries use built-in OpenAI/);assert.match(html,/configured Responses provider without credentials/);assert.match(html,/unavailable definition prevents Start/);
 assert.match(html,/value="nonloopback-anonymous"/);assert.match(html,/value="chosen-model"/);
});

const props=node=>node[Object.keys(node).find(k=>k.startsWith('__reactProps$'))];
const nodes=(c,tag)=>c.querySelectorAll(node=>node.localName===tag);
const region=(c,label)=>c.querySelectorAll(node=>node.getAttribute('aria-label')===label)[0];
const button=(c,label)=>nodes(c,'button').find(node=>node.textContent===label);
const labelled=(c,tag,label)=>nodes(c,tag).find(node=>node.parentNode.textContent.startsWith(label));
const change=(node,value)=>React.act(()=>props(node).onChange({target:{value}}));
const press=(c,label)=>React.act(async()=>{const node=button(c,label);assert.ok(node,label);assert.equal(!!props(node).disabled,false,label);await props(node).onClick();});
async function joinedPeer(changed='credentialed') {
 const directory=mkdtempSync(`${out}/joined-`);let sequence=0,ended=false,output='';
 const child=spawn('cargo',['test','--offline','--locked','--lib','access_provider_configured_observation_mounted_join','--','--test-threads=1'],{cwd:new URL('src-tauri/',app),env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true',CHIRALITY_PROVIDER_JOIN:directory,CHIRALITY_PROVIDER_JOIN_CHANGE:changed},stdio:['ignore','pipe','pipe']});
 child.stdout.on('data',data=>output+=data);child.stderr.on('data',data=>output+=data);
 const exited=new Promise(resolve=>child.on('close',code=>{ended=true;resolve(code);}));
 const read=async(name)=>{const deadline=Date.now()+120000;while(!existsSync(`${directory}/${name}`)){assert.equal(ended,false,output);assert.ok(Date.now()<deadline,`fixture timeout ${name}`);await new Promise(resolve=>setTimeout(resolve,5));}return JSON.parse(readFileSync(`${directory}/${name}`,'utf8'));};
 const send=(command,args)=>{const id=sequence++;const temporary=`${directory}/input.tmp`;writeFileSync(temporary,JSON.stringify({command,args}));renameSync(temporary,`${directory}/command-${id}.json`);return id;};
 const initial=await read('ready.json');
 return {initial,async call(command,args){const result=await read(`response-${send(command,args)}.json`);assert.doesNotMatch(JSON.stringify(result),/INVENTED_PRIVATE_PROVIDER_CANARY_481|RowSecret37/);return result;},async close(){if(!ended)send('finish',{});assert.equal(await exited,0,output);rmSync(directory,{recursive:true});}};
}
async function mountedChooser(native, handler, check, extra={}) {
 const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);const calls=[];
 let snapshot={...native.initial,...extra,roleLimits:{account:{roles:[]}},roleSet:{available:true,defaultRole:'HELP_HUMAN',roles:[{name:'HELP_HUMAN',meaning:'fixture role',default_for_new_chat:true}]}};
 const setSnapshot=value=>{snapshot=value;};
 const idle=installIdleNativeWaiting(async(command,args)=>{
  calls.push({command,args:structuredClone(args)});
  if(command==='host_status')return structuredClone(snapshot);
  if(command==='decision_view')return {rows:[]};
  if(command==='native_confirmation_content')return [];
  if(command==='provider_endpoint_discard' && handler.endpointCleanup!==true)return null;
  return handler(command,args,{get snapshot(){return snapshot;},setSnapshot});
 });
 const intervals=new Map(),previous={setInterval:globalThis.setInterval,clearInterval:globalThis.clearInterval};let timer=0;
 globalThis.setInterval=fn=>{intervals.set(++timer,fn);return timer;};globalThis.clearInterval=id=>intervals.delete(id);
 try{await React.act(()=>root.render(React.createElement(App)));await check(c,calls,{get snapshot(){return snapshot;},setSnapshot,async refresh(){await React.act(async()=>{for(const fn of intervals.values())await fn();});}});}
 finally{const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);Object.assign(globalThis,previous);assert.equal(intervals.size,0);}
}
test('actual private Peer read reaches mounted explicit provider choice then SAME source fresh Start refuses changed configuration',async()=>{
 const native=await joinedPeer();let latest;
 try{await mountedChooser(native,async(command,args,view)=>{
  assert.ok(['read_configured_providers','thread_start'].includes(command));
  const result=await native.call(command,args);latest=result;
  view.setSnapshot({...view.snapshot,...result.host,roleSet:view.snapshot.roleSet,roleLimits:view.snapshot.roleLimits});
  if(!result.response.ok)throw Error(result.response.error);
  return result.response.value;
 },async(c,calls)=>{
  const read=()=>button(c,'Read configured local providers');
  assert.ok(read());assert.equal(calls.filter(call=>call.command==='read_configured_providers').length,0);
  await change(labelled(c,'input','Model '),'person-chosen-model');await change(labelled(c,'input','Configured Codex provider '),'manual-before-read');
  const conversation=c.querySelectorAll(node=>node.getAttribute('id')==='conversation')[0];
  await change(labelled(conversation,'textarea','Text '),'Unsent global TEXT quartz fixture');
  await press(c,'Read configured local providers');
  assert.equal(props(labelled(c,'input','Configured Codex provider ')).value,'manual-before-read');
  assert.equal(props(labelled(c,'select','Access entry ')).value,'');
  assert.equal(latest.host.clientRequests.length,1);assert.equal(latest.host.clientRequests[0].method,'config/read');
  assert.equal(nodes(region(c,'Configured local providers'),'button').filter(node=>node.textContent.startsWith('Choose provider ')).length,1);
  await press(c,'Choose provider anonymous');
  assert.equal(props(labelled(c,'input','Model ')).value,'person-chosen-model');
  assert.equal(props(labelled(c,'input','Configured Codex provider ')).value,'anonymous');
  assert.equal(props(labelled(c,'select','Access entry ')).value,'local-provider');
  await press(c,'Start thread');
  assert.match(c.textContent,/credential element; no thread\/start sent/);
  assert.equal(latest.host.clientRequests.filter(call=>call.method==='config/read').length,2,'fresh current read after actual row choice');
  assert.equal(latest.host.clientRequests.filter(call=>call.method==='thread/start').length,0);
  assert.equal(props(labelled(c,'input','Model ')).value,'person-chosen-model');
  assert.equal(props(labelled(conversation,'textarea','Text ')).value,'Unsent global TEXT quartz fixture');
  assert.doesNotMatch(c.textContent,/INVENTED_PRIVATE_PROVIDER_CANARY_481|RowSecret37/);
  assert.ok(calls.every(call=>['host_status','decision_view','native_confirmation_content','read_configured_providers','thread_start'].includes(call.command)));
 });}finally{await native.close();}
});
test('superseding real config read retires row and Start handlers while an explicit manual choice remains independent',async()=>{
 const native=await joinedPeer('unchanged');let latest;
 try{await mountedChooser(native,async(command,args,view)=>{
  const result=await native.call(command,args);latest=result;view.setSnapshot({...view.snapshot,...result.host,roleSet:view.snapshot.roleSet,roleLimits:view.snapshot.roleLimits});
  if(!result.response.ok)throw Error(result.response.error);return result.response.value;
 },async(c,calls,view)=>{
  await change(labelled(c,'input','Model '),'explicit-current-model');await press(c,'Read configured local providers');
  const oldChoose=props(button(c,'Choose provider anonymous')).onClick;await press(c,'Choose provider anonymous');
  const oldStart=props(button(c,'Start thread')).onClick;
  const newer=await native.call('read_configured_providers',{generation:native.initial.generation,modeHomeClass:'account'});
  view.setSnapshot({...view.snapshot,...newer.host,roleSet:view.snapshot.roleSet,roleLimits:view.snapshot.roleLimits});await view.refresh();
  assert.equal(button(c,'Choose provider anonymous'),undefined);assert.equal(props(button(c,'Start thread')).disabled,true);
  await React.act(async()=>{oldChoose();await oldStart();});
  assert.equal(calls.filter(call=>call.command==='thread_start').length,0,'retained callbacks cannot authorize against a newer revision');
  await change(labelled(c,'input','Configured Codex provider '),'anonymous');
  assert.equal(props(button(c,'Start thread')).disabled,false,'explicit manual editing leaves listing authority behind');
  await press(c,'Start thread');
  assert.equal(latest.host.clientRequests.filter(row=>row.method==='config/read').length,3);
  assert.equal(latest.host.clientRequests.filter(row=>row.method==='thread/start').length,1);
  assert.match(c.textContent,/outcome unknown; no automatic retry/);
  assert.equal(props(labelled(c,'input','Model ')).value,'explicit-current-model');
 });}finally{await native.close();}
});
test('read failures and malformed projections cannot echo diagnostics, restore old rows or erase newer manual input',async()=>{
 for(const bad of ['error','malformed']) {
  const native=await joinedPeer();let release,ready;
  const waiting=new Promise(resolve=>ready=resolve);let reads=0;
  try{await mountedChooser(native,async(command,args,view)=>{
   assert.equal(command,'read_configured_providers');const result=await native.call(command,args);
   view.setSnapshot({...view.snapshot,...result.host,roleSet:view.snapshot.roleSet,roleLimits:view.snapshot.roleLimits});
   if(++reads===1)return result.response.value;
   ready();return new Promise((resolve,reject)=>release=()=>bad==='error'?reject(Error(canary)):resolve({state:canary,rows:[{id:canary}]}));
  },async(c,calls)=>{
   await change(labelled(c,'input','Model '),'old-model');await press(c,'Read configured local providers');
   const staleChoose=props(button(c,'Choose provider anonymous')).onClick;
   let pending;await React.act(async()=>{pending=props(button(c,'Read configured local providers')).onClick();await waiting;});
   assert.equal(button(c,'Choose provider anonymous'),undefined);
   await change(labelled(c,'input','Model '),'newer-model');await change(labelled(c,'input','Configured Codex provider '),'newer-manual');await change(labelled(c,'select','Access entry '),'local-provider');
   assert.equal(props(button(c,'Start thread')).disabled,true,'pending read prevents avoidable overlap');
   await React.act(async()=>{release();await pending;staleChoose();});
   assert.equal(props(labelled(c,'input','Model ')).value,'newer-model');assert.equal(props(labelled(c,'input','Configured Codex provider ')).value,'newer-manual');
   assert.equal(props(button(c,'Start thread')).disabled,false,'failed listing does not veto separately explicit manual Start');
   assert.equal(button(c,'Choose provider anonymous'),undefined);assert.match(c.textContent,/private diagnostic withheld/);assert.doesNotMatch(c.textContent,new RegExp(canary));
   assert.equal(calls.filter(call=>call.command==='thread_start').length,0);
  });}finally{await native.close();}
 }
});
test('late rows cannot survive an away/back home epoch, full generation restart or changed project scope',async()=>{
 for(const changeSource of ['home-away-back','generation','project','not-ready']) {
  const native=await joinedPeer();let release,ready;
  const waiting=new Promise(resolve=>ready=resolve);
  try{await mountedChooser(native,async(command,args,view)=>{
   if(command==='select_home'){view.setSnapshot({...view.snapshot,homeRouting:{...view.snapshot.homeRouting,activeModeHomeClass:args.modeHomeClass}});return {};}
   assert.equal(command,'read_configured_providers');const result=await native.call(command,args);
   view.setSnapshot({...view.snapshot,...result.host,homeRouting:{activeModeHomeClass:'account',entries:[{modeHomeClass:'account'},{modeHomeClass:'api-key'}]},roleSet:view.snapshot.roleSet,roleLimits:view.snapshot.roleLimits});
   ready();return new Promise(resolve=>release=()=>resolve(result.response.value));
  },async(c,calls,view)=>{
   let pending;await React.act(async()=>{pending=props(button(c,'Read configured local providers')).onClick();await waiting;});
   if(changeSource==='home-away-back'){await press(c,'Use api-key home');await press(c,'Use account home');}
   else{view.setSnapshot(changeSource==='generation'?{...view.snapshot,generation:{...view.snapshot.generation,spawnCounter:2}}:changeSource==='project'?{...view.snapshot,currentAppProjectContext:{reference:'/invented/different-project'}}:{...view.snapshot,state:'absent'});await view.refresh();}
   await change(labelled(c,'input','Model '),'newer-source-model');await change(labelled(c,'input','Configured Codex provider '),'newer-source-provider');
   await React.act(async()=>{release();await pending;});
   assert.equal(button(c,'Choose provider anonymous'),undefined);assert.equal(props(labelled(c,'input','Model ')).value,'newer-source-model');assert.equal(props(labelled(c,'input','Configured Codex provider ')).value,'newer-source-provider');
   assert.equal(calls.filter(call=>call.command==='read_configured_providers').length,1,'no automatic read on source changes');assert.equal(calls.filter(call=>call.command==='thread_start').length,0);
  },{homeRouting:{activeModeHomeClass:'account',entries:[{modeHomeClass:'account'},{modeHomeClass:'api-key'}]}});}finally{await native.close();}
 }
});
test('configured observation and explicit row choice preserve A-C-B-D composers, global TEXT and ordinary model override',async()=>{
 const native=await joinedPeer(),g=native.initial.generation,key=id=>JSON.stringify([g,id]);
 const thread=id=>({generation:g,threadId:id,model:'reported',modelProvider:'configured',appRole:{standing:'app-observed',role:null},roleRelation:{kind:'start'},futureGuidanceNotices:[]});
 const extra={threads:['A','B','C','D'].map(thread),workflowRoot:{context:{sourceRef:'original-workflow-source',generation:g,historyEpoch:1},projectLibraryAvailable:true,drafts:{drafts:[]},pendingTrials:[{reference:'trial:original',sequence:1,kind:'delegated',draftName:'method',location:'project',content:{value:'draft-bytes'},textIdentity:{value:'trial-bytes'},text:'Original trial text',message:'Original message',authoring:{generation:g,threadId:'B'},workFolder:'.chirality/workflow-trials/test',state:'pre-filled'}]}};
 try{await mountedChooser(native,async(command,args,view)=>{
  assert.equal(command,'read_configured_providers');const result=await native.call(command,args);
  view.setSnapshot({...view.snapshot,...result.host,...extra,roleSet:view.snapshot.roleSet,roleLimits:view.snapshot.roleLimits});return result.response.value;
 },async(c,calls)=>{
  const conversation=()=>c.querySelectorAll(node=>node.getAttribute('id')==='conversation')[0];
  const choose=id=>change(nodes(conversation(),'select')[0],key(id));
  await choose('A');await change(labelled(conversation(),'textarea','Text '),'Original unsent global TEXT é / 家');
  await change(labelled(conversation(),'input','Optional model identifier for next ordinary text turn '),'ordinary-A-only');
  await change(labelled(c,'select','Workflow chat '),'C');await change(labelled(c,'select','Authoring conversation '),key('B'));
  await change(labelled(c,'input','Model '),'explicit-new-model');
  await choose('B');const original=region(c,'Trial composer');assert.ok(original,'original B composer must be mounted before provider observation');
  await change(nodes(original,'textarea')[0],'Original B edit');await change(labelled(original,'select','Send to '),key('D'));
  await choose('A');await change(labelled(conversation(),'input','Optional model identifier for next ordinary text turn '),'ordinary-A-only');
  await press(c,'Read configured local providers');await press(c,'Choose provider anonymous');
  assert.equal(props(nodes(conversation(),'select')[0]).value,key('A'));assert.equal(props(labelled(c,'select','Workflow chat ')).value,'C');assert.equal(props(labelled(c,'select','Authoring conversation ')).value,key('B'));
  assert.equal(props(labelled(conversation(),'textarea','Text ')).value,'Original unsent global TEXT é / 家');
  assert.equal(props(labelled(conversation(),'input','Optional model identifier for next ordinary text turn ')).value,'ordinary-A-only');
  assert.equal(props(labelled(c,'input','Model ')).value,'explicit-new-model');
  await press(c,'View prepared message in conversation B');assert.equal(region(c,'Trial composer'),original);assert.equal(props(nodes(original,'textarea')[0]).value,'Original B edit');assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));
  assert.ok(calls.every(call=>['host_status','decision_view','native_confirmation_content','read_configured_providers'].includes(call.command)));
 },extra);}finally{await native.close();}
});
test('pending Start and pending observation reject retained opposite-action callbacks without extra dispatch',async()=>{
 const native=await joinedPeer('unchanged');let releaseRead,readReady,releaseStart,startReady;
 const reading=new Promise(resolve=>readReady=resolve),starting=new Promise(resolve=>startReady=resolve);
 try{await mountedChooser(native,async(command,args,view)=>{
  const result=await native.call(command,args);view.setSnapshot({...view.snapshot,...result.host,roleSet:view.snapshot.roleSet,roleLimits:view.snapshot.roleLimits});
  if(command==='read_configured_providers'){readReady();return new Promise(resolve=>releaseRead=()=>resolve(result.response.value));}
  assert.equal(command,'thread_start');startReady();return new Promise((_,reject)=>releaseStart=()=>reject(Error(result.response.error)));
 },async(c,calls)=>{
  await change(labelled(c,'input','Model '),'chosen-model');await change(labelled(c,'input','Configured Codex provider '),'anonymous');await change(labelled(c,'select','Access entry '),'local-provider');
  const oldStart=props(button(c,'Start thread')).onClick,oldRead=props(button(c,'Read configured local providers')).onClick;
  let read;await React.act(async()=>{read=oldRead();await reading;});
  await React.act(async()=>{await oldStart();});assert.equal(calls.filter(call=>call.command==='thread_start').length,0);
  await React.act(async()=>{releaseRead();await read;});
  let start;await React.act(async()=>{start=props(button(c,'Start thread')).onClick();await starting;});
  await React.act(async()=>{await oldRead();});assert.equal(calls.filter(call=>call.command==='read_configured_providers').length,1);
  await React.act(async()=>{releaseStart();await start;});
  assert.match(c.textContent,/outcome unknown/);assert.equal(props(button(c,'Start thread')).disabled,false);
 });}finally{await native.close();}
});

async function endpointPeer(mode='ok') {
 const directory=mkdtempSync(`${out}/endpoint-`);let sequence=0,ended=false,output='';
 const child=spawn('cargo',['test','--offline','--locked','--lib','access_provider_endpoint_mounted_join','--','--test-threads=1'],{cwd:new URL('src-tauri/',app),env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true',CHIRALITY_ENDPOINT_JOIN:directory,CHIRALITY_ENDPOINT_MODE:mode},stdio:['ignore','pipe','pipe']});
 child.stdout.on('data',data=>output+=data);child.stderr.on('data',data=>output+=data);
 const exited=new Promise(resolve=>child.on('close',code=>{ended=true;resolve(code);}));
 const read=async name=>{const deadline=Date.now()+120000;while(!existsSync(`${directory}/${name}`)){assert.equal(ended,false,output);assert.ok(Date.now()<deadline,`endpoint fixture timeout ${name}`);await new Promise(resolve=>setTimeout(resolve,5));}const packet=JSON.parse(readFileSync(`${directory}/${name}`,'utf8'));assert.doesNotMatch(JSON.stringify(packet),/INVENTED_PRIVATE/);return packet;};
 const send=(command,args)=>{const id=sequence++;writeFileSync(`${directory}/input.tmp`,JSON.stringify({command,args}));renameSync(`${directory}/input.tmp`,`${directory}/command-${id}.json`);return id;};
 return {initial:await read('ready.json'),async call(command,args){return read(`response-${send(command,args)}.json`);},async close(){if(!ended)send('finish',{});assert.equal(await exited,0,output);rmSync(directory,{recursive:true});}};
}
const endpointHandler = native => Object.assign(async(command,args,view) => {
 assert.ok(['read_configured_providers','provider_endpoint_offer','provider_endpoint_save','provider_endpoint_discard','thread_start'].includes(command),command);
 const packet=await native.call(command,args);if(command!=='provider_endpoint_discard')view.setSnapshot({...view.snapshot,...packet.host,roleSet:view.snapshot.roleSet,roleLimits:view.snapshot.roleLimits});
 if(!packet.response.ok)throw Error(packet.response.error);return packet.response.value;
},{endpointCleanup:true});
const endpointRequests = snapshot => snapshot.clientRequests.filter(r=>r.method==='config/batchWrite');

test('actual private endpoint offer/write/two decisions join mounted editor and fresh Root consumers without choosing or starting',async()=>{
 const native=await endpointPeer();
 try {await mountedChooser(native,endpointHandler(native),async(c,calls,view)=>{
  const model=labelled(c,'input','Model '),provider=labelled(c,'input','Configured Codex provider ');
  await change(model,'person-model');await change(provider,'manual-provider');await change(labelled(c,'select','Access entry '),'local-provider');
  const conversation=c.querySelectorAll(node=>node.getAttribute('id')==='conversation')[0];
  await change(labelled(conversation,'textarea','Text '),'Unsent endpoint fixture quartz');
  assert.equal(calls.filter(call=>call.command==='provider_endpoint_offer').length,0);
  await press(c,'Read configured local providers');await press(c,'Edit endpoint fixture.dot');
  assert.equal(calls.filter(call=>call.command==='provider_endpoint_offer').length,0,'opening the draft does not read native configuration');
  await change(labelled(c,'input','Endpoint URL '),'https://example.invalid/new');
  await press(c,'Review endpoint change');
  assert.equal(calls.filter(call=>call.command==='provider_endpoint_offer').length,1);
  assert.equal(endpointRequests(view.snapshot).length,0);
  assert.match(region(c,'Provider endpoint editor').textContent,/Current endpoint: https:\/\/example.invalid\/old/);
  await press(c,'Save endpoint…');
  assert.equal(endpointRequests(view.snapshot).length,1);assert.equal(view.snapshot.clientRequests.filter(r=>r.method==='config/read').length,3);
  assert.equal(view.snapshot.clientRequests.filter(r=>r.method==='thread/start').length,0);
  assert.match(region(c,'Provider endpoint editor').textContent,/current source continuation observed/);
  assert.equal(props(labelled(c,'input','Model ')).value,'person-model');assert.equal(props(labelled(c,'input','Configured Codex provider ')).value,'manual-provider');assert.equal(props(labelled(c,'select','Access entry ')).value,'local-provider');
  assert.equal(props(labelled(conversation,'textarea','Text ')).value,'Unsent endpoint fixture quartz');assert.doesNotMatch(c.textContent,/INVENTED_PRIVATE/);
  await change(labelled(c,'input','Configured Codex provider '),'fixture.dot');await press(c,'Start thread');
  assert.equal(view.snapshot.clientRequests.filter(r=>r.method==='config/read').length,4,'explicit later Start reads current configuration again');
  assert.equal(view.snapshot.clientRequests.filter(r=>r.method==='thread/start').length,1);assert.equal(endpointRequests(view.snapshot).length,1);
 });}finally{await native.close();}
});

for(const mode of ['cancel-before','cancel-after','error','timeout','override','ack-link-missing','ack-target-missing','override-link-missing','override-reread-timeout','override-reread-error'])test(`mounted endpoint ${mode} preserves choices and honest outcome without replay`,async()=>{
 const native=await endpointPeer(mode);
 try {await mountedChooser(native,endpointHandler(native),async(c,calls,view)=>{
  await change(labelled(c,'input','Model '),'person-model');await change(labelled(c,'input','Configured Codex provider '),'manual-provider');
  await press(c,'Read configured local providers');await press(c,'Edit endpoint fixture.dot');await change(labelled(c,'input','Endpoint URL '),'https://example.invalid/new');await press(c,'Review endpoint change');await press(c,'Save endpoint…');
  assert.equal(endpointRequests(view.snapshot).length,mode==='cancel-before'?0:1);
  const text=region(c,'Provider endpoint editor').textContent;
  assert.match(text,mode==='cancel-before'?/No endpoint write was sent/:mode==='override'||mode.startsWith('override-')?/override reported/:mode==='cancel-after'||mode.startsWith('ack-')?/source has not been continued/:/outcome unknown/);
  if(mode==='override'||mode.startsWith('override-'))assert.match(text,/source has not been continued/);
  assert.equal(button(c,'Save endpoint…'),undefined);assert.equal(props(labelled(c,'input','Model ')).value,'person-model');assert.equal(props(labelled(c,'input','Configured Codex provider ')).value,'manual-provider');
  assert.equal(view.snapshot.clientRequests.filter(r=>r.method==='thread/start').length,0);assert.doesNotMatch(c.textContent,/INVENTED_PRIVATE/);
 });}finally{await native.close();}
});

test('late actual endpoint offer cannot survive newer chooser input or erase its value',async()=>{
 const native=await endpointPeer();let release,offered,waiting;
 const held=new Promise(resolve=>release=resolve),started=new Promise(resolve=>waiting=resolve);
 const base=endpointHandler(native);
 const handler=Object.assign(async(command,args,view)=>{const result=await base(command,args,view);if(command==='provider_endpoint_offer'){offered=result;waiting();await held;}return result;},{endpointCleanup:true});
 try{await mountedChooser(native,handler,async(c,calls,view)=>{
  await press(c,'Read configured local providers');await press(c,'Edit endpoint fixture.dot');await change(labelled(c,'input','Endpoint URL '),'https://example.invalid/new');
  let pending;await React.act(async()=>{pending=props(button(c,'Review endpoint change')).onClick();await started;});
  await change(labelled(c,'input','Model '),'newer-person-model');
  await React.act(async()=>{release();await pending;});
  assert.equal(button(c,'Save endpoint…'),undefined);assert.equal(props(labelled(c,'input','Model ')).value,'newer-person-model');
  assert.equal(props(labelled(c,'input','Endpoint URL ')).value,'https://example.invalid/new');
  const replay=await native.call('provider_endpoint_save',{token:offered.token});assert.equal(replay.response.ok,false);assert.equal(endpointRequests(replay.host).length,0);
 });}finally{release();await native.close();}
});

test('endpoint editor cannot transfer a pending row or callback across chooser away/back',async()=>{
 const native=await endpointPeer();
 try{await mountedChooser(native,endpointHandler(native),async(c,calls,view)=>{
  await press(c,'Read configured local providers');await press(c,'Edit endpoint fixture.dot');await change(labelled(c,'input','Endpoint URL '),'https://example.invalid/new');await press(c,'Review endpoint change');
  const old=view.snapshot;
  view.setSnapshot({...old,homeRouting:{...old.homeRouting,activeModeHomeClass:'api-key'}});await view.refresh();
  view.setSnapshot(old);await view.refresh();
  assert.equal(region(c,'Provider endpoint editor'),undefined);assert.equal(button(c,'Save endpoint…'),undefined);
  assert.equal(endpointRequests(view.snapshot).length,0);assert.equal(view.snapshot.clientRequests.filter(r=>r.method==='thread/start').length,0);
 });}finally{await native.close();}
});

test('continued endpoint source does not admit Start from its offer or reread when the next actual private configuration is credentialed',async()=>{
 const native=await endpointPeer('start-credentialed');
 try{await mountedChooser(native,endpointHandler(native),async(c,calls,view)=>{
  await change(labelled(c,'input','Model '),'person-model');await change(labelled(c,'input','Configured Codex provider '),'fixture.dot');await change(labelled(c,'select','Access entry '),'local-provider');
  await press(c,'Read configured local providers');await press(c,'Edit endpoint fixture.dot');await change(labelled(c,'input','Endpoint URL '),'https://example.invalid/new');await press(c,'Review endpoint change');await press(c,'Save endpoint…');
  assert.match(region(c,'Provider endpoint editor').textContent,/current source continuation observed/);
  await press(c,'Start thread');
  assert.equal(view.snapshot.clientRequests.filter(r=>r.method==='config/read').length,4);
  assert.equal(view.snapshot.clientRequests.filter(r=>r.method==='thread/start').length,0);
  assert.equal(props(labelled(c,'input','Model ')).value,'person-model');assert.equal(props(labelled(c,'input','Configured Codex provider ')).value,'fixture.dot');assert.doesNotMatch(c.textContent,/INVENTED_PRIVATE/);
 });}finally{await native.close();}
});
