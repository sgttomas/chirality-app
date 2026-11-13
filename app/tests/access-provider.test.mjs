// Actual private Host/refusal publication -> the maintained visible consumers.
// Invented peer/files only; no supplier/model/human-act qualification.
import {test,after} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,mkdtempSync,rmSync} from 'node:fs';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
import {tmpdir} from 'node:os';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {localRequire} from './support/load-src.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
import './support/rust-prebuild.mjs';
const app=new URL('../',import.meta.url),out=mkdtempSync(`${tmpdir()}/access-provider-private-`);
const document=installMiniDom();
const {createRoot}=await import('react-dom/client');
const {App,EffectiveAccessSettingsPanel}=loadSrc('App');
after(()=>rmSync(out,{recursive:true}));
const url=new URL('src/ConversationRoles.tsx',app),compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});
const exports={};new Function('require','exports',compiled.outputText)(localRequire(createRequire(url)),exports);
const h=(c,p)=>renderToStaticMarkup(React.createElement(c,p));
const canary='INVENTED_PRIVATE_PROVIDER_CANARY_481';
let settingsPacket;
const settingsHost = () => ({state:'ready',generationClosed:false,generation:settingsPacket.scope.generation,
 homeRouting:{activeModeHomeClass:'account'},accessSettingsReadRevision:null,currentAppProjectContext:{reference:'/invented/work'}});
async function mountedSettings(handler,check) {
 const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c),calls=[];
 let host=settingsHost(),navigating=false;
 const render=()=>root.render(React.createElement(EffectiveAccessSettingsPanel,{host,navigating,refresh:async()=>{
  host={...host,accessSettingsReadRevision:settingsPacket.scope.readRevision};render();return structuredClone(host);
 }}));
 const idle=installIdleNativeWaiting(async(command,args)=>{calls.push({command,args});assert.equal(command,'read_effective_access_settings');return handler(command,args);});
 try {await React.act(render);await check(c,calls,async(next,nav=false)=>{host=next;navigating=nav;await React.act(render);});}
 finally {const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);}
}
test('effective access settings actual private Host projection reaches explicit mounted product control',async()=>{
 execFileSync('cargo',['test','--offline','--locked','--lib','access_settings_actual_projection_is_allowlisted_and_has_no_auth_or_model_calls','--','--test-threads=1'],{cwd:new URL('src-tauri/',app),env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CHIRALITY_TEST_OUTPUT_DIRECTORY:out},stdio:'inherit'});
 settingsPacket=JSON.parse(readFileSync(`${out}/access-settings.json`,'utf8'));
 let failure=false;
 await mountedSettings(async()=>{if(failure)throw Error(canary);return structuredClone(settingsPacket);},async(c,calls)=>{
  assert.equal(calls.length,0,'no automatic settings or authentication reads');
  await press(c,'Read effective storage and plugin settings');
  assert.deepEqual(calls[0].args,{generation:settingsPacket.scope.generation,modeHomeClass:'account'});
  assert.match(c.textContent,/Credential storage: file/);assert.match(c.textContent,/Plugins: false/);
  assert.match(c.textContent,/User configuration \(layer 1\)/);assert.match(c.textContent,/does not prove credential custody/);
  assert.doesNotMatch(c.textContent,/INVENTED_PRIVATE|config.toml|developer_instructions/);
  failure=true;await press(c,'Read effective storage and plugin settings');
  assert.doesNotMatch(c.textContent,/Credential storage: file/);assert.match(c.textContent,/private diagnostic withheld/);assert.doesNotMatch(c.textContent,new RegExp(canary));
 });
});
test('effective access settings unknown values and sources never become defaults or raw metadata',async()=>{
 const packet=structuredClone(settingsPacket);
 packet.credentialStore={state:'reported',value:canary,source:{state:'reported',kind:canary,layerIndex:canary}};
 packet.plugins={state:'unknown',value:false,source:{state:'unknown',path:canary}};
 await mountedSettings(async()=>packet,async(c)=>{
  await press(c,'Read effective storage and plugin settings');
  assert.match(c.textContent,/Credential storage: Unknown \/ not exposed/);assert.match(c.textContent,/Plugins: Unknown \/ not exposed/);
  assert.match(c.textContent,/Source: Unknown \/ not established/);assert.doesNotMatch(c.textContent,new RegExp(canary));
 });
});
test('effective access settings retire on newer reads, home changes and replacement generations',async()=>{
 await mountedSettings(async()=>structuredClone(settingsPacket),async(c,calls,update)=>{
  const old=props(button(c,'Read effective storage and plugin settings')).onClick;
  await press(c,'Read effective storage and plugin settings');
  await update({...settingsHost(),accessSettingsReadRevision:'newer-read'});
  assert.doesNotMatch(c.textContent,/Credential storage: file/);
  await update({...settingsHost(),homeRouting:{activeModeHomeClass:'api-key'}});
  await update(settingsHost());
  await React.act(async()=>{await old();});assert.equal(calls.length,1,'old home callback cannot make another read');
  await press(c,'Read effective storage and plugin settings');assert.match(c.textContent,/Credential storage: file/);
  await update({...settingsHost(),generation:{...settingsPacket.scope.generation,spawnCounter:2}});
  assert.doesNotMatch(c.textContent,/Credential storage: file/);
 });
});
test('effective access settings cannot revive after an obsolete status revision returns',async()=>{
 await mountedSettings(async()=>structuredClone(settingsPacket),async(c,calls,update)=>{
  await press(c,'Read effective storage and plugin settings');
  assert.match(c.textContent,/Credential storage: file/);
  await update({...settingsHost(),accessSettingsReadRevision:'newer-read'});
  assert.doesNotMatch(c.textContent,/Credential storage: file/);
  await update({...settingsHost(),accessSettingsReadRevision:settingsPacket.scope.readRevision});
  assert.doesNotMatch(c.textContent,/Credential storage: file/,'a delayed status cannot restore the retired observation');
  assert.equal(calls.length,1);
 });
});
test('effective access settings late reply cannot survive navigation away and back or a changed source',async()=>{
 for(const change of ['home','generation','navigation']) {
  let release,pending;
  await mountedSettings(()=>new Promise(resolve=>{release=resolve;}),async(c,calls,update)=>{
   await React.act(()=>{pending=props(button(c,'Read effective storage and plugin settings')).onClick();});
   assert.equal(calls.length,1);
   if(change==='home')await update({...settingsHost(),homeRouting:{activeModeHomeClass:'api-key'}});
   else if(change==='generation')await update({...settingsHost(),generation:{...settingsPacket.scope.generation,spawnCounter:2}});
   else await update(settingsHost(),true);
   await update(settingsHost());
   await React.act(async()=>{release(structuredClone(settingsPacket));await pending;});
   assert.doesNotMatch(c.textContent,/Credential storage: file/);assert.match(c.textContent,/No current settings observation/);
   assert.equal(calls.length,1);
  });
 }
});
test('effective access settings delayed read remembers an intervening revision',async()=>{
 let release,pending;
 await mountedSettings(()=>new Promise(resolve=>{release=resolve;}),async(c,calls,update)=>{
  await React.act(()=>{pending=props(button(c,'Read effective storage and plugin settings')).onClick();});
  await update({...settingsHost(),accessSettingsReadRevision:'newer-read'});
  await update({...settingsHost(),accessSettingsReadRevision:settingsPacket.scope.readRevision});
  await React.act(async()=>{release(structuredClone(settingsPacket));await pending;});
  assert.doesNotMatch(c.textContent,/Credential storage: file/,'an old status must not erase an intervening superseding read');
  assert.equal(calls.length,1);
 });
});
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

const props=node=>node[Object.keys(node).find(k=>k.startsWith('__reactProps$'))];
const nodes=(c,tag)=>c.querySelectorAll(node=>node.localName===tag);
const button=(c,label)=>nodes(c,'button').find(node=>node.textContent===label);
const labelled=(c,tag,label)=>nodes(c,tag).find(node=>node.parentNode.textContent.startsWith(label));
const change=(node,value)=>React.act(()=>props(node).onChange({target:{value}}));
const press=(c,label)=>React.act(async()=>{const node=button(c,label);assert.ok(node,label);assert.equal(!!props(node).disabled,false,label);await props(node).onClick();});
async function mountedChooser(native, handler, check) {
 const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);const calls=[];
 let snapshot={...native.initial,roleLimits:{account:{roles:[]}},roleSet:{available:true,defaultRole:'HELP_HUMAN',roles:[{name:'HELP_HUMAN',meaning:'fixture role',default_for_new_chat:true}]}};
 const setSnapshot=value=>{snapshot=value;};
 const idle=installIdleNativeWaiting(async(command,args)=>{
  calls.push({command,args:structuredClone(args)});
  if(command==='host_status')return handler.hostStatus ? handler.hostStatus(snapshot) : structuredClone(snapshot);
  if(command==='decision_view')return {rows:[]};
  if(command==='native_confirmation_content')return [];
  return handler(command,args,{get snapshot(){return snapshot;},setSnapshot});
 });
 const intervals=new Map(),previous={setInterval:globalThis.setInterval,clearInterval:globalThis.clearInterval};let timer=0;
 globalThis.setInterval=fn=>{intervals.set(++timer,fn);return timer;};globalThis.clearInterval=id=>intervals.delete(id);
 try{await React.act(()=>root.render(React.createElement(App)));await check(c,calls,{get snapshot(){return snapshot;},setSnapshot,async refresh(){await React.act(async()=>{for(const fn of intervals.values())await fn();});}});}
 finally{const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);Object.assign(globalThis,previous);assert.equal(intervals.size,0);}
}
test('effective access settings refresh cannot overwrite a newer App status',async()=>{
 let deferNext=false,releaseStatus;
 const handler=async(command,args,view)=>{
  assert.equal(command,'read_effective_access_settings');
  view.setSnapshot({...view.snapshot,accessSettingsReadRevision:settingsPacket.scope.readRevision,configurationProblem:'OLDER_SETTINGS_STATUS_R1'});
  return structuredClone(settingsPacket);
 };
 handler.hostStatus=snapshot=>{
  const captured=structuredClone(snapshot);
  if(deferNext){deferNext=false;return new Promise(resolve=>{releaseStatus=()=>resolve(captured);});}
  return captured;
 };
 await mountedChooser({initial:settingsHost()},handler,async(c,calls,view)=>{
  let pending;deferNext=true;
  await React.act(()=>{pending=props(button(c,'Read effective storage and plugin settings')).onClick();});
  assert.equal(typeof releaseStatus,'function');
  view.setSnapshot({...view.snapshot,accessSettingsReadRevision:'newer-read',configurationProblem:'LATEST_SETTINGS_STATUS_R2'});
  await view.refresh();
  assert.match(c.textContent,/LATEST_SETTINGS_STATUS_R2/);
  await React.act(async()=>{releaseStatus();await pending;});
  assert.match(c.textContent,/LATEST_SETTINGS_STATUS_R2/,'late explicit refresh must not overwrite the newer App snapshot');
  assert.doesNotMatch(c.textContent,/OLDER_SETTINGS_STATUS_R1|Credential storage: file/);
 });
});
// The account home's one connection route: the built-in OpenAI provider with the ChatGPT account entry.
const ROUTE='Use my ChatGPT account (built-in OpenAI)';
test('Start says why it is unavailable until the built-in route and a model are chosen',async()=>{
 const generation={appSession:'invented-session',home:'invented-account-home',spawnCounter:1};
 await mountedChooser({initial:{state:'ready',generationClosed:false,generation,homeRouting:{activeModeHomeClass:'account'},threads:[]}},async command=>{throw Error(`unexpected ${command}`);},async(c,calls)=>{
  const why=()=>c.querySelectorAll(node=>node.getAttribute('id')==='start-conversation-blocked')[0]?.textContent;
  assert.equal(props(button(c,'Start thread')).disabled,true);assert.match(why(),/Choose how this conversation connects \(step 1\)/);
  assert.equal(props(button(c,'Start thread'))['aria-describedby'],'start-conversation-blocked');
  await change(labelled(c,'input','Model '),'person-model');
  assert.match(why(),/Choose how this conversation connects \(step 1\)/,'a typed model without a route is not enough');
  await change(labelled(c,'input','Model '),'');
  await press(c,ROUTE);
  assert.equal(props(button(c,'Start thread')).disabled,true);assert.match(why(),/Choose a model \(step 2\)/);
  await change(labelled(c,'input','Model '),'person-model');
  assert.equal(props(button(c,'Start thread')).disabled,false);assert.equal(why(),undefined,'no reason is shown while Start is available');
  assert.equal(props(button(c,'Start thread'))['aria-describedby'],undefined);
  assert.equal(calls.filter(call=>!['host_status','decision_view','native_confirmation_content'].includes(call.command)).length,0,'choosing issues nothing');
 });
});
