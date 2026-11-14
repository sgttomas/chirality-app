import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
import './support/rust-prebuild.mjs';

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
const {App, FIRST_READ_PATIENCE_MS} = loadSrc('App');
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
    for(const label of ['Desktop setup action','Shared config.toml','Shared AGENTS.md','Shared skills directory','Project on next launch']) assert.equal(props(field(c,label)).value,'');
    assert.equal(field(c,'Supplier for next launch'),undefined,'the production supplier is fixed; no sole-option selector');
    assert.match(c.textContent,/Codex: the copy included with this App\./);
    assert.equal(props(button(c,'Review setup effects')).disabled,true);
    assert.equal(button(c,'Prepare home and save for next launch'),undefined);
    assert.match(c.textContent,/imports no credentials/);
    assert.match(c.textContent,new RegExp(packet.initial.supplier.path.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')));
    assert.match(c.textContent,/not authenticated qualification/);
    assert.equal(nodes(region(c,'Desktop setup inputs'),'select').length,2,'action and project only; no supplier/model/provider/role choice');
    assert.doesNotMatch(c.textContent,/does not exist yet|type where it should be/,'no guidance to type a nonexistent path');
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
    // Plus the App's one automatic settings read when Codex is ready.
    assert.ok(calls.every(c=>['host_status','decision_view','native_confirmation_content','desktop_setup_project_preview','desktop_setup_prepare','read_effective_access_settings'].includes(c.command)));
    idle.assertClean(c);
  } finally { const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);Object.assign(globalThis,previous);assert.equal(timers.size,0); }
});

// The existing miniDOM has no browser focus engine. Record focus() calls on
// mounted elements; this verifies intent/target, not AppKit or visual layout.
const focused=[];
Object.getPrototypeOf(document.createElement('p')).focus=function(){focused.push(this);};
const guidance=c=>c.querySelectorAll(n=>n.getAttribute('id')==='desktop-setup-next-step')[0];
const deferred=()=>{let resolve,reject;const promise=new Promise((yes,no)=>{resolve=yes;reject=no;});return {promise,resolve,reject};};

test('setup explains incomplete choices, focuses real preview and edit returns without saving',async()=>{
  await mountedPanel(packet.initial,command=>{
    assert.equal(command,'desktop_setup_preview');return packet.preview;
  },async(c,calls)=>{
    assert.match(guidance(c).textContent,/Choose first-time setup, or keep your current sign-in/);
    const needs=region(c,'What setup needs').textContent;
    for(const words of [/new, empty folder for its Codex sign-in/,/doesn't copy or reuse sign-ins/,/links to them rather than copying/,/project folder \(optional\)/,/quit and open the App again/])assert.match(needs,words);
    assert.equal(props(button(c,'Review setup effects'))['aria-describedby'],'desktop-setup-next-step');
    assert.deepEqual(nodes(c,'legend').map(n=>n.textContent),['1. Sign-in and shared settings','2. Project and Codex']);
    await change(field(c,'Desktop setup action'),'new');assert.match(guidance(c).textContent,/Choose your config.toml, AGENTS.md and skills folder/);
    await explicitInputs(c);assert.match(guidance(c).textContent,/ready to review/);
    await press(c,'Review setup effects');assert.equal(focused.at(-1).textContent,'Review before saving');
    const savedPath=props(field(c,'Shared config.toml')).value;
    await press(c,'Edit setup choices');assert.equal(region(c,'Desktop setup effects'),undefined);
    assert.equal(focused.at(-1),button(c,'Review setup effects'));
    assert.equal(props(field(c,'Shared config.toml')).value,savedPath);
    assert.deepEqual(calls.map(c=>c.command),['desktop_setup_preview']);
  });
});

test('pending review and native save report progress and refuse duplicate retained callbacks',async()=>{
  const checking=deferred(),saving=deferred();
  await mountedPanel(packet.initial,command=>{
    if(command==='desktop_setup_preview')return checking.promise;
    if(command==='desktop_setup_prepare')return saving.promise;
    assert.fail(command);
  },async(c,calls)=>{
    await explicitInputs(c);
    const review=props(button(c,'Review setup effects')).onClick;
    let first;await React.act(()=>{first=review();void review();});
    assert.equal(calls.length,1);assert.match(guidance(c).textContent,/Checking the selected locations/);
    assert.equal(props(region(c,'Desktop setup inputs'))['aria-busy'],true);
    assert.ok(nodes(c,'fieldset').every(n=>props(n).disabled));
    await React.act(async()=>{checking.resolve(packet.preview);await first;});
    const confirm=props(button(c,packet.preview.affirmative)).onClick;
    let second;await React.act(()=>{second=confirm();void confirm();});
    assert.equal(calls.length,2);assert.match(guidance(c).textContent,/native confirmation/);
    assert.equal(props(button(c,'Edit setup choices')).disabled,true,'local Edit cannot dismiss a native question');
    await React.act(()=>props(region(c,'Desktop setup effects')).onKeyDown({key:'Escape',preventDefault(){assert.fail('must not consume native Escape');},stopPropagation(){assert.fail('must not consume native Escape');}}));
    assert.equal(calls.length,2);assert.ok(region(c,'Desktop setup effects'));
    await React.act(async()=>{saving.resolve(packet.saved);await second;});
    assert.match(focused.at(-1).textContent,/saved for your next launch/);
    assert.equal(props(focused.at(-1)).role,'status');
    assert.equal(props(region(c,'Desktop setup inputs'))['aria-busy'],false);
    assert.match(c.textContent,/Current launch: setup-required/);
  });
});

test('failed review is announced, retains inputs and retries only on explicit action',async()=>{
  let count=0;
  await mountedPanel(packet.initial,command=>{
    assert.equal(command,'desktop_setup_preview');if(++count===1)throw Error('source is unavailable');return packet.preview;
  },async(c,calls)=>{
    await explicitInputs(c);await press(c,'Review setup effects');
    assert.equal(props(focused.at(-1)).role,'alert');assert.match(focused.at(-1).textContent,/source is unavailable/);
    assert.equal(calls.length,1);assert.equal(region(c,'Desktop setup effects'),undefined);
    await press(c,'Review setup effects');assert.equal(calls.length,2);assert.ok(region(c,'Desktop setup effects'));
  });
});

test('Escape leaves only local review; picker cancel preserves choices and native cancel cannot imply a save',async()=>{
  await mountedPanel(packet.initial,command=>{
    if(command==='desktop_setup_pick')return null;
    if(command==='desktop_setup_preview')return packet.preview;
    if(command==='desktop_setup_prepare')return {state:'cancelled; setup unchanged'};
    assert.fail(command);
  },async(c,calls)=>{
    await explicitInputs(c);const path=props(field(c,'Shared config.toml')).value;
    await press(c,'Browse Shared config.toml');assert.equal(props(field(c,'Shared config.toml')).value,path);
    await press(c,'Review setup effects');
    let prevented=false;await React.act(()=>props(region(c,'Desktop setup effects')).onKeyDown({key:'Escape',preventDefault(){prevented=true;},stopPropagation(){}}));
    assert.equal(prevented,true);assert.equal(region(c,'Desktop setup effects'),undefined);assert.equal(focused.at(-1),button(c,'Review setup effects'));
    assert.equal(calls.filter(c=>c.command==='desktop_setup_prepare').length,0);
    await press(c,'Review setup effects');await press(c,packet.preview.affirmative);
    assert.equal(region(c,'Pending desktop setup'),undefined);assert.match(focused.at(-1).textContent,/cancelled; setup unchanged/);
    assert.equal(props(field(c,'Shared config.toml')).value,path);
  });
});

// First use: the focused welcome over the actual native packets (new App-owned
// settings preview and saved state from the executed Rust producer).
const {FirstUseSetup}=loadSrc('FirstUse');
async function mountedWelcome(view, handler, check) {
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
  const previous=window.__TAURI_INTERNALS__;const calls=[];
  window.__TAURI_INTERNALS__={invoke:async(command,args)=>{calls.push({command,args:structuredClone(args)});return handler(command,args);}};
  try { await React.act(()=>root.render(React.createElement(React.StrictMode,null,React.createElement(FirstUseSetup,{view})))); await check(c,calls); }
  finally { await React.act(()=>root.unmount());document.body.removeChild(c);window.__TAURI_INTERNALS__=previous; }
}
test('first use: choose a project, start with new App-owned settings, review the host effects and confirm',async()=>{
  const next=packet.newSettings;
  await mountedWelcome(packet.initial,(command,args)=>{
    if(command==='desktop_setup_pick'){assert.deepEqual(args,{kind:'project'});return {displayPath:textPath(next.project),nativePath:next.project};}
    if(command==='desktop_setup_new_settings_preview'){assert.deepEqual(args,{projectPath:next.project},'only the chosen project; no settings, home or supplier nomination');return next.preview;}
    if(command==='desktop_setup_prepare'){assert.deepEqual(args,{previewToken:next.preview.token});return next.saved;}
    assert.fail(command);
  },async(c,calls)=>{
    const welcome=region(c,'Welcome');assert.match(welcome.textContent,/Welcome to Chirality/);
    assert.equal(nodes(c,'select').length,0,'no technical drop-downs on first use');
    assert.equal(field(c,'Your config.toml'),undefined,'paths only appear for existing settings');
    assert.doesNotMatch(c.textContent,/Keep my current sign-in/,'an unavailable keep-account route is not offered');
    assert.doesNotMatch(c.textContent.replace(/Technical details[^]*$/,''),/Retaining an account requires|owner-use development|walking skeleton/,'diagnostics stay in technical details');
    assert.match(guidance2(c).textContent,/Choose the folder you want to work in/);
    assert.equal(props(button(c,'Review setup')).disabled,true);
    assert.equal(props(field(c,'Project folder')).value,'','no project location is proposed');
    await press(c,'Browse…');
    assert.equal(props(field(c,'Project folder')).value,textPath(next.project));
    assert.match(guidance2(c).textContent,/Ready to review\. Nothing is created or saved until you confirm/);
    await press(c,'Review setup');
    const effects=region(c,'What setup will do').textContent;
    for(const effect of next.preview.effects)assert.ok(effects.includes(effect),effect);
    assert.match(effects,/Create a new settings folder for this App/);assert.match(effects,/No other Codex settings, home or credential is read, imported or changed/);
    await press(c,'Create settings and save for next launch…');
    assert.match(region(c,'Setup saved').textContent,/quit Chirality \(⌘Q\) and open it again.*Connection & access.*ChatGPT account or prepare the oMLX connection/);
    assert.deepEqual(calls.map(call=>call.command),['desktop_setup_pick','desktop_setup_new_settings_preview','desktop_setup_prepare']);
  });
});
test('first use: no project, existing settings route, cancel and change keep choices and never save',async()=>{
  await mountedWelcome(packet.initial,(command,args)=>{
    if(command==='desktop_setup_preview'){assert.deepEqual(args,{sharedPaths:packet.inputs.shared,projectPath:null,supplierSelection:packet.initial.supplier.selection});return packet.preview;}
    if(command==='desktop_setup_prepare')return {state:'cancelled; no setup paths or saved request changed'};
    assert.fail(command);
  },async(c,calls)=>{
    await press(c,'Continue without a project');
    assert.match(region(c,'Welcome').textContent,/No project for now/);
    const existing=nodes(c,'input').find(n=>props(n).type==='radio'&&n.parentNode.textContent.startsWith(' Use my existing Codex settings'));
    await React.act(()=>props(existing).onChange());
    assert.equal(props(button(c,'Review setup')).disabled,true,'existing settings need all three');
    for(const [i,label] of ['Your config.toml','Your AGENTS.md','Your skills folder'].entries())await change(field(c,label),textPath(packet.inputs.shared[i]));
    await press(c,'Review setup');assert.ok(region(c,'What setup will do'));
    await press(c,'Prepare home and save for next launch…');
    assert.match(c.textContent,/Not saved — you cancelled in the dialog\. Your choices are still here\./);
    assert.equal(region(c,'Setup saved'),undefined);
    assert.equal(props(field(c,'Your config.toml')).value,textPath(packet.inputs.shared[0]));
    await press(c,'Review setup');await press(c,'Change my choices');assert.equal(region(c,'What setup will do'),undefined);
    assert.deepEqual(calls.map(call=>call.command),['desktop_setup_preview','desktop_setup_prepare','desktop_setup_preview']);
  });
});
// Typed project folder: the same field shows and sends one project choice.
const projectBytes=text=>({encoding:'unix_bytes',bytes:Array.from(new TextEncoder().encode(text))});
const routeRadio=(c,start)=>nodes(c,'input').find(n=>props(n).type==='radio'&&n.parentNode.textContent.startsWith(start));
const typedProject='/invented/My Project ~ $HOME/日本語 é e\u0301 😀 ';
test('first use: a typed absolute project folder reaches each route\'s existing preview exactly as typed and saves only after review',async()=>{
  const routes=[
    {view:packet.initial,route:null,command:'desktop_setup_new_settings_preview',args:{projectPath:projectBytes(typedProject)},preview:packet.newSettings.preview,saved:packet.newSettings.saved},
    {view:packet.retained.initial,route:' Keep my current sign-in',command:'desktop_setup_project_preview',args:{projectPath:projectBytes(typedProject)},preview:packet.retained.preview,saved:packet.retained.saved},
    {view:packet.initial,route:' Use my existing Codex settings',command:'desktop_setup_preview',args:{sharedPaths:packet.inputs.shared,projectPath:projectBytes(typedProject),supplierSelection:packet.initial.supplier.selection},preview:packet.preview,saved:packet.saved},
  ];
  for(const r of routes) await mountedWelcome(r.view,(command,args)=>{
    if(command===r.command){assert.deepEqual(args,r.args,'typed bytes are not trimmed, expanded or resolved');return r.preview;}
    if(command==='desktop_setup_prepare'){assert.deepEqual(args,{previewToken:r.preview.token});return r.saved;}
    assert.fail(command);
  },async(c,calls)=>{
    const input=field(c,'Project folder');
    assert.equal(input.localName,'input');assert.equal(props(input).id,'first-use-project');
    assert.match(region(c,'Welcome').textContent,/Type or paste the folder's full path, or use Browse… to choose it/);
    assert.equal(props(button(c,'Browse…'))['aria-label'],'Browse for project folder');
    await change(input,typedProject);
    assert.equal(props(field(c,'Project folder')).value,typedProject);
    assert.equal(props(field(c,'Project folder'))['aria-invalid'],undefined);
    if(r.route) await React.act(()=>props(routeRadio(c,r.route)).onChange());
    if(r.command==='desktop_setup_preview') for(const [i,label] of ['Your config.toml','Your AGENTS.md','Your skills folder'].entries())await change(field(c,label),textPath(packet.inputs.shared[i]));
    assert.match(guidance2(c).textContent,/Ready to review/);
    await press(c,'Review setup');assert.ok(region(c,'What setup will do'));
    await press(c,r.preview.affirmative+'…');
    assert.ok(region(c,'Setup saved'));
    assert.deepEqual(calls.map(call=>call.command),[r.command,'desktop_setup_prepare']);
  });
});
test('first use: invalid or incomplete project text cannot be reviewed, even by a retained Review handler',async()=>{
  await mountedWelcome(packet.initial,command=>assert.fail(`no IPC for an incomplete project: ${command}`),async(c,calls)=>{
    await change(field(c,'Project folder'),'/invented/valid');
    const staleReview=props(button(c,'Review setup')).onClick;
    for(const [text,words] of [['relative/dir',/full path, starting with \//],['~/Projects',/aren't expanded or looked up/],['$HOME/work',/full path, starting with \//],[' /invented/leading-space',/full path, starting with \//],['/invented/a\0b',/cannot be used in a folder path/],['/invented/\ud800',/incomplete character/],['/invented/\udc00',/incomplete character/]]){
      await change(field(c,'Project folder'),text);
      assert.equal(props(field(c,'Project folder')).value,text,'the literal text stays as typed');
      assert.equal(props(field(c,'Project folder'))['aria-invalid'],true);
      assert.match(props(field(c,'Project folder'))['aria-describedby'],/first-use-project-problem/);
      assert.match(region(c,'Welcome').textContent,words);
      assert.match(guidance2(c).textContent,/Check the project folder path/);
      assert.equal(props(button(c,'Review setup')).disabled,true);
      await React.act(async()=>{await props(button(c,'Review setup')).onClick();});
    }
    await change(field(c,'Project folder'),'');
    assert.equal(props(field(c,'Project folder'))['aria-invalid'],undefined);
    assert.match(guidance2(c).textContent,/Choose the folder you want to work in/);
    assert.equal(props(button(c,'Review setup')).disabled,true);
    await React.act(async()=>{await props(button(c,'Review setup')).onClick();await staleReview();});
    assert.deepEqual(calls,[]);
  });
});
test('first use: project edits and no-project invalidate a rendered or in-flight review',async()=>{
  const next=packet.newSettings;let checking=deferred();
  await mountedWelcome(packet.initial,(command,args)=>{
    if(command==='desktop_setup_new_settings_preview')return checking.promise;
    if(command==='desktop_setup_prepare')assert.fail('no confirmation of an invalidated review');
    assert.fail(command);
  },async(c,calls)=>{
    await change(field(c,'Project folder'),'/invented/first');
    let first;await React.act(()=>{first=props(button(c,'Review setup')).onClick();});
    assert.equal(props(field(c,'Project folder')).disabled,true);
    await change(field(c,'Project folder'),'/invented/second');
    await React.act(async()=>{checking.resolve(next.preview);await first;});
    assert.equal(region(c,'What setup will do'),undefined,'a review of the earlier text is not shown');
    assert.equal(props(field(c,'Project folder')).value,'/invented/second');
    checking=deferred();let second;await React.act(()=>{second=props(button(c,'Review setup')).onClick();});
    await React.act(()=>props(button(c,'Continue without a project')).onClick());
    await React.act(async()=>{checking.resolve(next.preview);await second;});
    assert.equal(region(c,'What setup will do'),undefined);
    assert.match(region(c,'Welcome').textContent,/No project for now/);
    assert.equal(props(field(c,'Project folder')).value,'');
    checking=deferred();checking.resolve(next.preview);
    await press(c,'Review setup');assert.ok(region(c,'What setup will do'));
    const staleConfirm=props(button(c,next.preview.affirmative+'…')).onClick;
    await change(field(c,'Project folder'),'/invented/third');
    assert.equal(region(c,'What setup will do'),undefined,'editing the project discards the rendered review');
    assert.doesNotMatch(region(c,'Welcome').textContent,/No project for now/);
    await React.act(async()=>{await staleConfirm();});
    assert.deepEqual(calls.map(call=>[call.command,call.args.projectPath]),[
      ['desktop_setup_new_settings_preview',projectBytes('/invented/first')],
      ['desktop_setup_new_settings_preview',projectBytes('/invented/second')],
      ['desktop_setup_new_settings_preview',null],
    ]);
  });
});
test('first use: Browse cancel keeps typed text; a picked folder sends its untouched native reference until the field is edited',async()=>{
  const native={displayPath:'Selected folder with an unreadable name',nativePath:{encoding:'unix_bytes',bytes:[47,105,110,118,47,120,255]}};
  let picked=null;
  await mountedWelcome(packet.initial,command=>{
    if(command==='desktop_setup_pick')return picked;
    if(command==='desktop_setup_new_settings_preview')return packet.newSettings.preview;
    assert.fail(command);
  },async(c,calls)=>{
    await change(field(c,'Project folder'),'/invented/typed');
    await press(c,'Browse…');
    assert.equal(props(field(c,'Project folder')).value,'/invented/typed','cancel keeps the typed choice');
    picked=native;await press(c,'Browse…');
    assert.equal(props(field(c,'Project folder')).value,native.displayPath);
    await press(c,'Review setup');assert.ok(region(c,'What setup will do'));
    assert.equal(props(field(c,'Project folder'))['aria-invalid'],undefined,'picked display text is not validated as a typed path');
    await change(field(c,'Project folder'),'/invented/edited');
    assert.equal(region(c,'What setup will do'),undefined);
    await press(c,'Review setup');
    await press(c,'Continue without a project');picked=native;await press(c,'Browse…');
    assert.doesNotMatch(region(c,'Welcome').textContent,/No project for now/);
    await press(c,'Review setup');
    const previews=calls.filter(call=>call.command==='desktop_setup_new_settings_preview').map(call=>call.args.projectPath);
    assert.deepEqual(previews,[native.nativePath,projectBytes('/invented/edited'),native.nativePath],'the display text is never re-encoded as the picked reference');
  });
});
test('first use: a later project edit or no-project supersedes an in-flight Browse',async()=>{
  const native={displayPath:'/invented/picked',nativePath:projectBytes('/invented/picked')};
  for(const later of ['typed','none']){
    const picking=deferred();
    await mountedWelcome(packet.initial,command=>{
      if(command==='desktop_setup_pick')return picking.promise;
      if(command==='desktop_setup_new_settings_preview')return packet.newSettings.preview;
      assert.fail(command);
    },async(c,calls)=>{
      let pending;await React.act(()=>{pending=props(button(c,'Browse…')).onClick();});
      assert.equal(props(button(c,'Review setup')).disabled,true);assert.equal(props(button(c,'Browse…')).disabled,true);
      if(later==='typed') await change(field(c,'Project folder'),'/invented/typed-later');
      else await React.act(()=>props(button(c,'Continue without a project')).onClick());
      await React.act(async()=>{picking.resolve(native);await pending;});
      assert.equal(props(field(c,'Project folder')).value,later==='typed'?'/invented/typed-later':'');
      await press(c,'Review setup');
      assert.deepEqual(calls,[
        {command:'desktop_setup_pick',args:{kind:'project'}},
        {command:'desktop_setup_new_settings_preview',args:{projectPath:later==='typed'?projectBytes('/invented/typed-later'):null}},
      ],'the late picker result never replaces the later choice');
    });
  }
});
test('a saved setup whose Codex home is held is not shown as setup being needed',async()=>{
  const reason='Desktop request unavailable: Codex was not started on this home: the home is held by another process on this computer. If another Chirality App is using it, use that App or quit it first.';
  const view={...packet.dataHeld,launch:{state:'home-held',reason,operationalData:'not admitted; nothing operational started'}};
  await mountedWelcome(view,()=>assert.fail('no IPC while a home is held'),async(c,calls)=>{
    const welcome=region(c,'Welcome');
    assert.match(welcome.textContent,/A Codex home this App uses is held/);
    assert.equal(c.querySelectorAll(n=>n.getAttribute('role')==='alert')[0].textContent,reason);
    assert.match(welcome.textContent,/Nothing operational was started\. This launch did not change your saved setup\. Quit this Chirality instance \(⌘Q\), then reopen it after the process holding the home has released it\./);
    assert.doesNotMatch(welcome.textContent,/saved setup is unchanged|open Chirality again when/,'no claim that nobody changed it, and the quit is said');
    assert.doesNotMatch(welcome.textContent,/Welcome to Chirality|choose a project folder|Set up your workspace/i,'setup is not offered or said to be needed');
    assert.equal(nodes(c,'button').length,0,'no setup action is offered');
    assert.deepEqual(calls,[]);
  });
});
test('a second App on data another process holds says what was observed, names no owner and offers no setup',async()=>{
  const view=packet.dataHeld;
  assert.equal(view.launch.state,'data-held');
  await mountedWelcome(view,()=>assert.fail('no IPC while another process holds this data'),async(c,calls)=>{
    const welcome=region(c,'Welcome');
    assert.match(welcome.textContent,/This App's data is in use/);
    assert.equal(c.querySelectorAll(n=>n.getAttribute('role')==='alert')[0].textContent,'Chirality did not start here: its data is held by another process on this computer. Nothing operational was started. If a Chirality window is already open, use it; otherwise quit whatever is using this data, then open Chirality again.');
    assert.doesNotMatch(welcome.textContent,/already running|another Chirality App|nothing was started or changed/i,'no owner, window or unchanged state is asserted');
    assert.equal(nodes(c,'button').length,0,'no setup action is offered');
    assert.deepEqual(calls,[]);
  });
});
test('the mounted App shows only the welcome while setup is required and keeps confirmation content visible',async()=>{
  const host={state:'setup-required',generation:null,threads:[],desktopSetup:packet.initial,roleLimits:{account:{roles:[]}}};
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
  const timers=new Map();let timer=0;const previous={setInterval:globalThis.setInterval,clearInterval:globalThis.clearInterval};
  globalThis.setInterval=(fn,ms)=>{const id=++timer;timers.set(id,{fn,ms});return id;};globalThis.clearInterval=id=>timers.delete(id);
  const idle=installIdleNativeWaiting(async(command)=>{
    if(command==='host_status')return structuredClone(host);if(command==='decision_view')return {rows:[]};if(command==='native_confirmation_content')return [];
    assert.fail(`Unexpected IPC: ${command}`);
  });
  const hiddenUp=node=>{for(let n=node;n;n=n.parentNode)if(props(n)?.hidden)return true;return false;};
  try {
    await React.act(()=>root.render(React.createElement(App)));
    assert.ok(region(c,'Welcome'));assert.equal(hiddenUp(region(c,'Welcome')),false);
    for(const label of ['Workspace navigation','Workspace connection status','Run a workflow'])assert.equal(hiddenUp(region(c,label)),true,label);
    assert.equal(hiddenUp(region(c,'Content named by an open native confirmation')),false,'native confirmation content stays visible');
    host.state='ready';host.desktopSetup={...packet.retained.initial};host.generation={appSession:'s',home:'h',spawnCounter:1};
    await React.act(async()=>{for(const t of timers.values())await t.fn();});
    assert.equal(region(c,'Welcome'),undefined,'once admitted, the workspace returns');
    assert.equal(hiddenUp(region(c,'Workspace navigation')),false);
    idle.assertClean(c);
  } finally { const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);Object.assign(globalThis,previous); }
});
test('a refused start at launch is shown in the connection status with its reason, without pressing Start, only for its home and only while no start is under way',async()=>{
  const reason='Codex was not started on this home: the home is held by another process on this computer. If another Chirality App is using it, use that App or quit it first.';
  const host={state:'absent',generation:null,threads:[],desktopSetup:{...packet.retained.initial},codexHome:'app-home:invented-shown',lastStartRefusal:{reason,actor:'app-startup',at:'invented',home:'app-home:invented-shown',attempt:null},roleLimits:{account:{roles:[]}}};
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
  const timers=new Map();let timer=0;const previous={setInterval:globalThis.setInterval,clearInterval:globalThis.clearInterval};
  globalThis.setInterval=(fn,ms)=>{const id=++timer;timers.set(id,{fn,ms});return id;};globalThis.clearInterval=id=>timers.delete(id);
  const calls=[];
  const idle=installIdleNativeWaiting(async(command)=>{
    calls.push(command);
    if(command==='host_status')return structuredClone(host);if(command==='decision_view')return {rows:[]};if(command==='native_confirmation_content')return [];
    return null;
  });
  try {
    await React.act(()=>root.render(React.createElement(App)));
    const status=region(c,'Workspace connection status');
    assert.match(status.textContent,/Codex is not connected/);
    assert.equal(region(c,'Why Codex was not started').textContent,reason);
    assert.ok(!calls.includes('host_start'),'shown without a start being pressed');
    const poll=async()=>React.act(async()=>{for(const t of timers.values())await t.fn();});
    // A start under way: an earlier refusal is not shown beside it, even if a host still carried one.
    for(const state of ['verifying','spawning','handshaking','ready','stopping']){
      host.state=state;await poll();
      assert.equal(region(c,'Why Codex was not started'),undefined,state);
    }
    // A refusal for another home is not shown for this one.
    host.state='refused';host.lastStartRefusal={...host.lastStartRefusal,home:'app-home:invented-other'};await poll();
    assert.equal(region(c,'Why Codex was not started'),undefined,'another home');
    // A reason that does not say so itself is introduced as a refusal to start.
    host.lastStartRefusal={reason:'The Codex home does not exist, so Codex was not started on it.',home:'app-home:invented-shown',attempt:null};await poll();
    assert.equal(region(c,'Why Codex was not started').textContent,'Codex was not started: The Codex home does not exist, so Codex was not started on it.');
    host.state='ready';host.lastStartRefusal=null;host.generation={appSession:'s',home:'h',spawnCounter:1};
    await poll();
    assert.equal(region(c,'Why Codex was not started'),undefined,'gone once Codex is connected');
  } finally { const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);Object.assign(globalThis,previous); }
});
const guidance2=c=>c.querySelectorAll(n=>n.getAttribute('id')==='first-use-next')[0];

// Before the App's first host read: neither the welcome nor the workspace is in the document, only a
// line that says the App is starting; a failed first read says so and offers to try again.
async function mountedBeforeFirstRead(check) {
  const c=document.createElement('div');document.body.appendChild(c);const root=createRoot(c);
  const timers=new Map();let timer=0;const previous={setInterval:globalThis.setInterval,clearInterval:globalThis.clearInterval,setTimeout:globalThis.setTimeout,clearTimeout:globalThis.clearTimeout};
  globalThis.setInterval=(fn,ms)=>{const id=++timer;timers.set(id,{fn,ms});return id;};globalThis.clearInterval=id=>timers.delete(id);
  // The App's first-read patience timeout is held here and fired by the test; every other timeout runs as usual.
  const patience=new Map();
  globalThis.setTimeout=(fn,ms,...rest)=>{if(ms===FIRST_READ_PATIENCE_MS){const id={patience:++timer};patience.set(id,fn);return id;}return previous.setTimeout(fn,ms,...rest);};
  globalThis.clearTimeout=id=>{if(patience.has(id))patience.delete(id);else previous.clearTimeout(id);};
  const elapse=()=>React.act(async()=>{for(const fn of patience.values())fn();patience.clear();});
  const reads=[],calls=[];
  const idle=installIdleNativeWaiting(async(command)=>{
    calls.push(command);
    if(command==='host_status')return new Promise((resolve,reject)=>reads.push({resolve,reject}));
    if(command==='decision_view')return {rows:[]};if(command==='native_confirmation_content')return [];
    assert.fail(`Unexpected IPC: ${command}`);
  });
  const poll=()=>React.act(async()=>{for(const t of timers.values())t.fn();});
  const settle=(outcome)=>React.act(async()=>{const read=reads.at(-1);if(outcome instanceof Error)read.reject(outcome);else read.resolve(structuredClone(outcome));});
  try { await React.act(()=>root.render(React.createElement(App))); await check({c,reads,calls,poll,settle,elapse,patience}); idle.assertClean(c); }
  finally { const text=c.textContent;await React.act(()=>root.unmount());document.body.removeChild(c);idle.restore(text);Object.assign(globalThis,previous); }
}
const starting=c=>c.querySelectorAll(n=>n.getAttribute('role')==='status'&&n.textContent==='Starting Chirality…');
const workspaceAbsent=(c,state)=>{
  assert.ok(!nodes(c,'h1').some(n=>n.textContent==='Chirality'),`${state}: the workspace heading is not in the document`);
  for(const label of ['Workspace navigation','Workspace connection status','Run a workflow','Workspace tools','Welcome'])assert.ok(!region(c,label),`${state}: ${label}`);
  assert.equal(c.querySelectorAll(n=>n.getAttribute('id')==='view-conversation').length,0,`${state}: no workspace view, hidden or not`);
};
const readyHost=()=>({state:'ready',generation:{appSession:'s',home:'h',spawnCounter:1},threads:[],desktopSetup:{...packet.retained.initial},roleLimits:{account:{roles:[]}}});

test('before the first host read, only the starting line is shown: no workspace heading or control, and no welcome',async()=>{
  await mountedBeforeFirstRead(async({c,reads})=>{
    assert.equal(reads.length,1,'the first read is under way');
    workspaceAbsent(c,'not yet read');
    assert.equal(nodes(c,'button').length,0,'no control can be reached or counted');
    assert.equal(starting(c).length,1,'one status line says the App is starting');
    const shown=nodes(c,'main')[0].childNodes.filter(n=>n.localName!=='style').map(n=>n.textContent).join('');
    assert.equal(shown,'Starting Chirality…','nothing else is shown');
  });
});

test('the first read decides: setup required shows the welcome with the workspace hidden, as before',async()=>{
  await mountedBeforeFirstRead(async({c,settle})=>{
    await settle({state:'setup-required',generation:null,threads:[],desktopSetup:packet.initial,roleLimits:{account:{roles:[]}}});
    assert.equal(starting(c).length,0);
    assert.ok(!!region(c,'Welcome'));
    assert.ok(nodes(c,'h1').some(n=>n.textContent==='Welcome to Chirality'));
    const hiddenUp=node=>{for(let n=node;n;n=n.parentNode)if(props(n)?.hidden)return true;return false;};
    for(const label of ['Workspace navigation','Workspace connection status','Run a workflow'])assert.equal(hiddenUp(region(c,label)),true,label);
  });
});

test('the first read decides: setup not required shows the workspace and no welcome',async()=>{
  await mountedBeforeFirstRead(async({c,settle})=>{
    await settle(readyHost());
    assert.equal(starting(c).length,0);
    assert.ok(!region(c,'Welcome'));
    const heading=nodes(c,'h1').find(n=>n.textContent==='Chirality');
    assert.ok(!!heading);
    for(let n=heading;n;n=n.parentNode)assert.notEqual(props(n)?.hidden,true,'the workspace is not hidden');
    assert.ok(!!region(c,'Workspace navigation'));
  });
});

test('a failed first read says so and offers to try again; loading never conceals it, and a later success shows the workspace',async()=>{
  await mountedBeforeFirstRead(async({c,reads,calls,poll,settle})=>{
    await settle(new Error('invented raw diagnostic'));
    workspaceAbsent(c,'failed');
    assert.equal(starting(c).length,0,'the starting line does not stand in for a failure');
    assert.equal(c.querySelectorAll(n=>n.getAttribute('role')==='alert')[0]?.textContent,'Chirality could not read its own state. It keeps trying; you can also try again now.');
    assert.doesNotMatch(c.textContent,/invented raw diagnostic/,'the raw diagnostic is not shown');
    assert.deepEqual(nodes(c,'button').map(n=>n.textContent),['Try again']);
    // A scheduled read that is still under way leaves the failure shown.
    await poll();
    assert.equal(reads.length,2);
    assert.ok(!!button(c,'Try again'),'still failed while a later read is under way');
    await settle(new Error('invented again'));
    assert.ok(!!button(c,'Try again'));
    const before=calls.filter(command=>command==='host_status').length;
    await React.act(async()=>{props(button(c,'Try again')).onClick();});
    assert.equal(calls.filter(command=>command==='host_status').length,before+1,'Try again makes the read again');
    await settle(readyHost());
    assert.ok(!button(c,'Try again'));
    assert.ok(nodes(c,'h1').some(n=>n.textContent==='Chirality'));
    assert.ok(!!region(c,'Workspace navigation'));
  });
});

test('a read that fails after one succeeded leaves the workspace shown, as before',async()=>{
  await mountedBeforeFirstRead(async({c,poll,settle})=>{
    await settle(readyHost());
    await poll();await settle(new Error('invented later failure'));
    assert.ok(nodes(c,'h1').some(n=>n.textContent==='Chirality'));
    assert.ok(!!region(c,'Workspace navigation'));
    assert.ok(!button(c,'Try again'));
  });
});

test('a first read that neither arrives nor fails: the starting line, then after the patience time the slow line with Try again; a read arriving later shows the page',async()=>{
  assert.equal(FIRST_READ_PATIENCE_MS,10000,"App Agent 0's number");
  const slowLine='Chirality is taking longer than usual to start. It keeps trying; you can also try again now.';
  const slow=c=>c.querySelectorAll(n=>n.getAttribute('role')==='status'&&n.textContent===slowLine);
  await mountedBeforeFirstRead(async({c,reads,calls,poll,settle,elapse,patience})=>{
    assert.equal(patience.size,1,'one patience timeout is set at launch');
    assert.equal(starting(c).length,1);assert.equal(slow(c).length,0);
    workspaceAbsent(c,'not yet read');assert.equal(nodes(c,'button').length,0);
    // The status timer keeps issuing reads while the first is unanswered.
    await poll();assert.equal(reads.length,2,'a new read starts while the first is unanswered');
    await elapse();
    assert.equal(starting(c).length,0,'the starting line is replaced');
    assert.equal(slow(c).length,1,'the slow line says the App is taking longer than usual');
    assert.equal(c.querySelectorAll(n=>n.getAttribute('role')==='alert').length,0,'nothing failed, so nothing says it did');
    workspaceAbsent(c,'slow');
    assert.deepEqual(nodes(c,'button').map(n=>n.textContent),['Try again']);
    const before=calls.filter(command=>command==='host_status').length;
    await React.act(async()=>{props(button(c,'Try again')).onClick();});
    assert.equal(calls.filter(command=>command==='host_status').length,before+1,'Try again issues a read while earlier ones are unanswered');
    workspaceAbsent(c,'slow after Try again');
    await settle(readyHost());
    assert.equal(slow(c).length,0);assert.ok(!button(c,'Try again'));
    assert.ok(nodes(c,'h1').some(n=>n.textContent==='Chirality'));
    assert.ok(!!region(c,'Workspace navigation'));assert.ok(!region(c,'Welcome'));
  });
});

test('after the patience time, a first read that arrives and needs setup shows the welcome as otherwise',async()=>{
  await mountedBeforeFirstRead(async({c,elapse,settle})=>{
    await elapse();
    await settle({state:'setup-required',generation:null,threads:[],desktopSetup:packet.initial,roleLimits:{account:{roles:[]}}});
    assert.ok(nodes(c,'h1').some(n=>n.textContent==='Welcome to Chirality'));
    assert.ok(!button(c,'Try again'));
    assert.equal(c.querySelectorAll(n=>n.getAttribute('role')==='status'&&/taking longer than usual/.test(n.textContent)).length,0);
  });
});
