import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';

// Actual native resolver/prepare/save packets. The filesystem fixture is
// invented and removed by Rust. No native App, supplier or model is launched.
const producer = 'desktop_startup::tests::mounted_setup_packets';
const result = spawnSync('cargo', ['test','--offline','--locked','--lib',producer,'--','--exact','--nocapture','--test-threads=1'], {
  cwd: fileURLToPath(new URL('../src-tauri/', import.meta.url)), encoding:'utf8', timeout:180000, maxBuffer:16*1024*1024,
  env:{...process.env, CHIRALITY_SKIP_CODEX:'1', CARGO_NET_OFFLINE:'true'},
});
assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);
assert.match(result.stdout,/test result: ok\. 1 passed; 0 failed;/);
const marker = result.stdout.match(/DESKTOP_SETUP_PACKETS=(\{[^\n]*\})/);
assert.ok(marker,'native packets must come from the executed test');
const packet = JSON.parse(marker[1]);
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {DesktopSetupPanel} = loadSrc('DesktopSetupPanel');
const {App} = loadSrc('App');
const props = node=>node[Object.keys(node).find(k=>k.startsWith('__reactProps$'))];
const nodes = (c,tag)=>c.querySelectorAll(node=>node.localName===tag);
const region = (c,label)=>c.querySelectorAll(node=>node.getAttribute('aria-label')===label)[0];
const button = (c,label)=>nodes(c,'button').find(node=>node.textContent===label);
const field = (c,label)=>region(c,label);
const labelled = (c,tag,label)=>nodes(c,tag).find(node=>node.parentNode.textContent.startsWith(label));
const change = (node,value)=>React.act(()=>props(node).onChange({target:{value}}));
const press = (c,label)=>React.act(async()=>{ const node=button(c,label); assert.ok(node,label); assert.equal(!!props(node).disabled,false,label); await props(node).onClick(); });
const textPath = path=>new TextDecoder().decode(new Uint8Array(path.bytes));
async function explicitInputs(c, project='none') {
  await change(field(c,'Desktop setup action'),'new');
  for (const [i,label] of ['Shared config.toml','Shared AGENTS.md','Shared skills directory'].entries()) await change(field(c,label),textPath(packet.inputs.shared[i]));
  await change(field(c,'Project on next launch'),project);
  if(project==='chosen') await change(field(c,'Next project directory'),textPath(packet.inputs.project));
  await change(field(c,'Supplier for next launch'),packet.initial.supplier.selection);
}
async function mountedPanel(view, handler, check) {
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
  const previous=window.__TAURI_INTERNALS__;const calls=[];
  window.__TAURI_INTERNALS__={invoke:async(command,args)=>{calls.push({command,args:structuredClone(args)});return handler(command,args);}};
  try { await React.act(()=>root.render(React.createElement(DesktopSetupPanel,{view}))); await check(c,calls); }
  finally { await React.act(()=>root.unmount());document.body.removeChild(c);window.__TAURI_INTERNALS__=previous; }
}

test('empty native setup shows explicit choices and never requests supplier/account/model defaults',async()=>{
  await mountedPanel(packet.initial,()=>assert.fail('no IPC on render'),async(c,calls)=>{
    assert.equal(props(region(c,'Desktop setup')).open,true);
    for(const label of ['Desktop setup action','Shared config.toml','Shared AGENTS.md','Shared skills directory','Project on next launch','Supplier for next launch']) assert.equal(props(field(c,label)).value,'');
    assert.equal(props(button(c,'Review setup effects')).disabled,true);
    assert.equal(button(c,'Prepare home and save for next launch'),undefined);
    assert.match(c.textContent,/imports no credentials/);
    assert.match(c.textContent,new RegExp(packet.initial.supplier.path.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
    assert.match(c.textContent,/not authenticated qualification/);
    assert.equal(nodes(region(c,'Desktop setup inputs'),'select').length,3,'action, project and supplier only; no model/provider/role choice');
    assert.deepEqual(calls,[]);
  });
});

test('review displays actual effects before explicit prepare and save remains pending until a fresh launch',async()=>{
  await mountedPanel(packet.initial,(command,args)=>{
    if(command==='desktop_setup_preview') { assert.deepEqual(args,{sharedPaths:packet.inputs.shared,projectPath:packet.inputs.project,supplierSelection:packet.initial.supplier.selection});return packet.preview; }
    if(command==='desktop_setup_prepare') { assert.deepEqual(args,{previewToken:packet.preview.token});return packet.saved; }
    assert.fail(command);
  },async(c,calls)=>{
    await explicitInputs(c,'chosen');await press(c,'Review setup effects');
    assert.equal(calls.length,1);assert.equal(calls[0].command,'desktop_setup_preview');
    for(const effect of packet.preview.effects) assert.ok(region(c,'Desktop setup effects').textContent.includes(effect));
    await press(c,'Prepare home and save for next launch');
    assert.equal(region(c,'Desktop setup effects'),undefined);
    assert.match(region(c,'Pending desktop setup').textContent,/Saved for next launch/);
    assert.ok(c.textContent.includes(packet.saved.pending.accountHome));
    assert.match(c.textContent,/Current launch: setup-required/);
    assert.match(c.textContent,/no automatic quit, restart, login, conversation or model selection/);
    assert.deepEqual(calls.map(c=>c.command),['desktop_setup_preview','desktop_setup_prepare']);
  });
  await mountedPanel(packet.fresh,()=>assert.fail('fresh packet must not request native actions'),async c=>{
    assert.match(c.textContent,/Current launch: saved-request/);assert.equal(props(region(c,'Desktop setup')).open,false);
    assert.match(region(c,'Current desktop resource metadata').textContent,/config.toml: Linked/);
  });
  await mountedPanel(packet.resourceLimits,()=>assert.fail('resource metadata display requests no native actions'),async c=>{
    const resources=region(c,'Current desktop resource metadata').textContent;
    assert.match(resources,/config.toml: TargetMissing/);assert.match(resources,/AGENTS.md: Conflict/);
    assert.match(resources,/does not establish native content discovery/);
  });
});

test('native picker retains lossless reference, edits invalidate review, and custody/save errors stay visible',async()=>{
  const native={displayPath:'/invented/display-only',nativePath:{encoding:'unix_bytes',bytes:[47,120,255]}};
  let fail=false;
  await mountedPanel(packet.busy,(command,args)=>{
    if(command==='desktop_setup_pick')return native;
    if(command==='desktop_setup_preview') { if(fail)throw Error(packet.busy.launch.reason); assert.deepEqual(args.sharedPaths[0],native.nativePath);return packet.preview; }
    if(command==='desktop_setup_prepare')throw Error('invented source changed after native question; saved request not replaced');
    assert.fail(command);
  },async(c,calls)=>{
    await explicitInputs(c);await press(c,'Browse Shared config.toml');
    assert.equal(props(field(c,'Shared config.toml')).value,native.displayPath);
    await press(c,'Review setup effects');
    await change(field(c,'Project on next launch'),'chosen');assert.equal(region(c,'Desktop setup effects'),undefined);
    await change(field(c,'Project on next launch'),'none');await press(c,'Review setup effects');
    await press(c,'Prepare home and save for next launch');
    assert.equal(region(c,'Pending desktop setup'),undefined);assert.match(c.textContent,/source changed after native question/);
    fail=true;await press(c,'Review setup effects');assert.ok(c.textContent.includes(packet.busy.launch.reason));
    assert.equal(region(c,'Desktop setup effects'),undefined);
    assert.ok(calls.every(c=>c.command.startsWith('desktop_setup_')));
  });
});

test('keep-account availability comes from admitted native packets and never supplies an implicit choice',async()=>{
  for(const view of [packet.initial,packet.environment,packet.busy,packet.retained.conflict]) await mountedPanel(view,()=>assert.fail('availability display performs no native action'),async(c,calls)=>{
    assert.equal(props(field(c,'Desktop setup action')).value,'');
    const retain=nodes(field(c,'Desktop setup action'),'option').find(node=>props(node).value==='retain');
    assert.equal(props(retain).disabled,true);assert.match(c.textContent,/Keep-account project change unavailable/);
    assert.deepEqual(calls,[]);
  });
  await mountedPanel(packet.retained.initial,()=>assert.fail('choosing form mode performs no native action'),async(c,calls)=>{
    await change(field(c,'Desktop setup action'),'retain');
    assert.equal(field(c,'Shared config.toml'),undefined);assert.equal(field(c,'Supplier for next launch'),undefined);
    assert.ok(c.textContent.includes(packet.retained.initial.retainProject.accountHome));
    assert.equal(props(field(c,'Project on next launch')).value,'');
    assert.equal(props(button(c,'Review setup effects')).disabled,true);
    assert.deepEqual(calls,[]);
  });
});

test('explicit keep-H project Q or absence reviews accurate effects and saves pending-only through project-only IPC',async()=>{
  for(const none of [false,true]) await mountedPanel(none?packet.retained.freshQ:packet.retained.initial,(command,args)=>{
    if(command==='desktop_setup_project_preview') {
      assert.deepEqual(args,{projectPath:none?null:packet.retained.project},'no renderer home/shared/supplier nomination');
      return none?packet.retained.nonePreview:packet.retained.preview;
    }
    if(command==='desktop_setup_prepare') {
      assert.deepEqual(args,{previewToken:(none?packet.retained.nonePreview:packet.retained.preview).token});
      return none?packet.retained.noneSaved:packet.retained.saved;
    }
    assert.fail(command);
  },async(c,calls)=>{
    await change(field(c,'Desktop setup action'),'retain');await change(field(c,'Project on next launch'),none?'none':'chosen');
    if(!none) await change(field(c,'Next project directory'),textPath(packet.retained.project));
    await press(c,'Review setup effects');
    const effects=region(c,'Desktop setup effects').textContent;
    assert.ok(effects.includes(packet.retained.preview.accountHome));
    assert.doesNotMatch(effects,/Create new account directory|Create config.toml link/);
    assert.equal(button(c,'Prepare home and save for next launch'),undefined);
    await press(c,'Save project for next launch');
    assert.match(region(c,'Pending desktop setup').textContent,/Pending project request only/);
    if(none) assert.match(region(c,'Pending desktop setup').textContent,/explicitly absent/);
    assert.match(c.textContent,/Current launch: saved-request/);
    assert.equal(props(button(c,'Review setup effects')).disabled,true,'a pending plan cannot be overwritten by another retained change');
    assert.deepEqual(calls.map(c=>c.command),['desktop_setup_project_preview','desktop_setup_prepare']);
  });
});

test('retained preview edits and actual stale/superseded confirmation errors produce no silent fallback or pending save',async()=>{
  await mountedPanel(packet.retained.initial,(command)=>{
    if(command==='desktop_setup_project_preview')return packet.retained.preview;
    if(command==='desktop_setup_prepare')throw Error(packet.retained.conflict.retainProject.reason);
    assert.fail(command);
  },async(c,calls)=>{
    await change(field(c,'Desktop setup action'),'retain');await change(field(c,'Project on next launch'),'none');
    await press(c,'Review setup effects');
    await change(field(c,'Project on next launch'),'chosen');assert.equal(region(c,'Desktop setup effects'),undefined);
    await change(field(c,'Next project directory'),textPath(packet.retained.project));await press(c,'Review setup effects');await press(c,'Save project for next launch');
    assert.ok(c.textContent.includes(packet.retained.conflict.retainProject.reason));
    assert.equal(region(c,'Pending desktop setup'),undefined);assert.equal(region(c,'Desktop setup effects'),undefined);
    assert.equal(props(field(c,'Desktop setup action')).value,'retain');
    assert.ok(calls.every(c=>['desktop_setup_project_preview','desktop_setup_prepare'].includes(c.command)));
  });
});

test('setup save in the mounted App preserves operational A, Workflow C, unsent TEXT and original composer B targeting D',async()=>{
  const g={appSession:'invented-desktop-ui',home:'invented-account',spawnCounter:1};
  const key=id=>JSON.stringify([g,id]);
  const thread=id=>({generation:g,threadId:id,model:'reported',modelProvider:'configured',appRole:{standing:'app-observed',role:null},roleRelation:{kind:'start'},futureGuidanceNotices:[]});
  const host={state:'ready',generation:g,threads:['A','B','C','D'].map(thread),roleLimits:{account:{roles:[]}},desktopSetup:packet.retained.initial,
    currentAppProjectContext:{reference:textPath(packet.retained.currentProject),sourceCaption:'explicit saved desktop project',standing:'frozen source fixture'},
    attachmentSelections:{launchAppProjectObservation:{nativeRoot:packet.retained.currentProject}},
    workflowRoot:{context:{sourceRef:'original-workflow-source',generation:g,historyEpoch:1},projectLibraryAvailable:true,drafts:{drafts:[]},pendingTrials:[{reference:'trial:original',sequence:1,kind:'delegated',draftName:'method',location:'project',content:{value:'draft-bytes'},textIdentity:{value:'trial-bytes'},text:'Original trial text',message:'Original message',authoring:{generation:g,threadId:'B'},workFolder:'.chirality/workflow-trials/test',state:'pre-filled'}]},
    homeRouting:{activeModeHomeClass:'account',entries:[{modeHomeClass:'account'}]}};
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);const calls=[];
  const timers=new Map();let timer=0;const previous={setInterval:globalThis.setInterval,clearInterval:globalThis.clearInterval};
  globalThis.setInterval=(fn,ms)=>{const id=++timer;timers.set(id,{fn,ms});return id;};globalThis.clearInterval=id=>timers.delete(id);
  const idle=installIdleNativeWaiting(async(command,args)=>{
    calls.push({command,args:structuredClone(args)});
    if(command==='host_status')return structuredClone(host);
    if(command==='decision_view')return {rows:[]};
    if(command==='native_confirmation_content')return [];
    if(command==='desktop_setup_project_preview')return packet.retained.preview;
    if(command==='desktop_setup_prepare'){host.desktopSetup={...packet.retained.initial,pending:packet.retained.saved.pending,retainProject:packet.retained.saved.retainProject};return packet.retained.saved;}
    assert.fail(`Unexpected IPC: ${command}`);
  });
  const conversation=()=>c.querySelectorAll(node=>node.getAttribute('id')==='conversation')[0];
  const choose=id=>change(nodes(conversation(),'select')[0],key(id));
  try {
    await React.act(()=>root.render(React.createElement(App)));
    await choose('A');await change(labelled(conversation(),'textarea','Text '),'Global unsent TEXT é / 家');
    await change(labelled(c,'select','Workflow chat '),'C');await change(labelled(c,'select','Authoring conversation '),key('B'));
    await change(labelled(c,'input','Model '),'explicit-model-stays');
    await choose('B');const original=region(c,'Trial composer');assert.ok(original);
    await change(nodes(original,'textarea')[0],'Edited original B');await change(labelled(original,'select','Send to '),key('D'));
    await choose('A');const setup=region(c,'Desktop setup');
    await change(field(setup,'Desktop setup action'),'retain');await change(field(setup,'Project on next launch'),'chosen');await change(field(setup,'Next project directory'),textPath(packet.retained.project));await press(setup,'Review setup effects');await press(setup,'Save project for next launch');
    assert.equal(props(nodes(conversation(),'select')[0]).value,key('A'));
    assert.equal(props(labelled(c,'select','Workflow chat ')).value,'C');assert.equal(props(labelled(c,'select','Authoring conversation ')).value,key('B'));
    assert.equal(props(labelled(conversation(),'textarea','Text ')).value,'Global unsent TEXT é / 家');
    assert.equal(props(labelled(c,'input','Model ')).value,'explicit-model-stays');
    assert.equal(host.currentAppProjectContext.reference,textPath(packet.retained.currentProject));
    assert.deepEqual(host.attachmentSelections.launchAppProjectObservation.nativeRoot,packet.retained.currentProject);
    assert.match(setup.textContent,/Current launch: saved-request/,'pending save must not replace active source status');
    await press(c,'View prepared message in conversation B');
    assert.equal(region(c,'Trial composer'),original,'same mounted composer owner');
    assert.equal(props(nodes(original,'textarea')[0]).value,'Edited original B');assert.equal(props(labelled(original,'select','Send to ')).value,key('D'));
    assert.ok(calls.every(c=>['host_status','decision_view','native_confirmation_content','desktop_setup_project_preview','desktop_setup_prepare'].includes(c.command)));
    idle.assertClean(c);
  } finally { const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);Object.assign(globalThis,previous);assert.equal(timers.size,0); }
});
