import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {localRequire} from './support/load-src.mjs';
const load=name=>{const url=new URL(`../src/${name}`,import.meta.url);const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});const exports={};new Function('require','exports',compiled.outputText)(localRequire(createRequire(url)),exports);return exports;};
const {RoleHeader,RoleChoice,RoleLimits,ROLE_PLAIN_MEANING,limitWords,ContinueAsPanel,SupplyStatus,NativeChildRoles,ChildAssociations,RoleLimitObservations,ModelProviderFields,guidanceChange,roleName,attemptSend,SendOutcome}=load('ConversationRoles.tsx');
const h=(c,p)=>renderToStaticMarkup(React.createElement(c,p));
const noop=()=>{};

const roles=JSON.parse(readFileSync(new URL('../src-tauri/resources/instructions/roles.json',import.meta.url),'utf8')).roles;
// DEL-02-04 TBD-004: for 4.0.0 the bundled set preselects HELP_HUMAN. A set with no default is exercised with an invented copy.
const roleSet={available:true,roles:roles.map(r=>({...r,default_for_new_chat:r.name==='HELP_HUMAN'})),defaultRole:'HELP_HUMAN'};
const bundled={available:true,roles,defaultRole:roles.find(r=>r.default_for_new_chat)?.name??null};
// The limit account as conversation_roles::limit_account hands it.
const all={limitId:'L-ALL-1',statement:"Work within the brief's write targets",standing:'stated-not-enforced',presentedAs:'Stated, not enforced',basis:'b',notEnforcement:['brief-text','worktree','sandbox','approval-policy']};
const task={limitId:'L-TASK-1',statement:'A task agent does not delegate',standing:'stated-not-enforced',presentedAs:'Stated, not enforced',basis:'b',notEnforcement:['approval-policy','sandbox','user-configuration','depth-limit']};
const limits={available:true,standing:'Stated in the role\'s guidance; Codex does not enforce it.',notRead:[],account:{roles:roles.map(r=>({role:r.name,meaning:r.meaning,delegation:r.delegation,guidanceState:'default',limits:r.name==='TASK'?[task,all]:[all]}))}};
const g={appSession:'s',home:'h',spawnCounter:1};
const thread=(over={})=>({generation:g,threadId:'thread',appRole:{standing:'app-observed',role:'HELP_HUMAN',supply_ref:'sup:1'},roleRelation:{kind:'start'},futureGuidanceNotices:[],...over});
const header=(t,calls={})=>h(RoleHeader,{thread:t,limits,busy:false,ready:true,continueAs:calls.continueAs??noop,fork:calls.fork??noop});

test('the header shows the fixed role, its limits as handed and the two ways on',()=>{
  const html=header(thread());
  assert.ok(html.includes('Role: <b>HELP_HUMAN</b>. It is fixed for this conversation&#x27;s life'));
  assert.ok(html.includes("Work within the brief&#x27;s write targets: <b>Stated, not enforced</b>"));
  assert.ok(html.includes('Continue as HELP_HUMAN…')&&html.includes('Fork (same role)'));
  assert.ok(html.includes('this conversation keeps its role'));
  assert.ok(!html.includes('Guidance changed since this conversation started'),'no change, no flag');
  const unknown=header(thread({appRole:{standing:'unknown',reason:'original App supply binding not established'},roleRelation:null}));
  assert.ok(unknown.includes('Role not established in this App process (original App supply binding not established)'));
  assert.equal(roleName({standing:'app-observed',role:null}),'No role');
});

test('the guidance-changed flag fires only on an actual change',()=>{
  const changed=header(thread({futureGuidanceNotices:[{path:'agents/AGENT_HELP_HUMAN.md',kind:'changed',reason:'guidance changed since this conversation started'}]}));
  assert.ok(changed.includes('<b>Guidance changed since this conversation started</b>: agents/AGENT_HELP_HUMAN.md (edited)'));
  assert.ok(changed.includes('Nothing was sent to this conversation; it keeps the guidance it started with.'));
  assert.equal((changed.match(/Continue as HELP_HUMAN…/g)??[]).length,2,'the flag offers Continue as the same role');
  const missing=header(thread({futureGuidanceNotices:[{path:'AGENTS.md',kind:'missing',reason:'missing'}]}));
  assert.ok(missing.includes('AGENTS.md (missing now)'));
  const unread=header(thread({futureGuidanceNotices:[{path:'AGENTS.md',kind:'not-read',reason:'unreadable: store unavailable'}]}));
  assert.ok(!unread.includes('Guidance changed since'),'a comparison not made is not a change');
  assert.ok(unread.includes('could not be read (AGENTS.md), so it was not compared'));
  assert.deepEqual(guidanceChange([{kind:'changed'},{kind:'not-read'},{kind:'missing'}]).changed.length,2);
  assert.deepEqual(guidanceChange(undefined),{changed:[],notRead:[]});
});

test('fork and continued-from relations are shown as relations; nothing changes the role',()=>{
  const fork=header(thread({roleRelation:{kind:'inherited-fork',sourceThread:'thread-a',sourceSupplyRef:'sup:a',forkedFromId:'thread-a'},threadId:'fork-1'}));
  assert.ok(fork.includes('Fork of conversation thread-a (same role)'));
  const cont=header(thread({roleRelation:{kind:'continued-from',from:{sourceThread:'thread-a',sourceRole:{standing:'app-observed',role:'WORKING_ITEMS',supply_ref:'sup:a'}}}}));
  assert.ok(cont.includes('Continues conversation thread-a (its role: WORKING_ITEMS); a relation only: no history was carried.'));
  // The App offers no control that changes a started conversation's role.
  // Continue as and fork are exercised through their commands in
  // conversation-panel, fork-admission and trial-continue-model-choice tests.
  const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8')+readFileSync(new URL('../src/ConversationRoles.tsx',import.meta.url),'utf8');
  assert.ok(!/thread\/settings\/update|developer_instructions|setRole\(selected/.test(app));
});

test('the start display is readable: preselection, no role, TASK not offered, limits as handed',()=>{
  const html=h(RoleChoice,{group:"start-thread-role",roleSet,limits,role:roleSet.defaultRole,setRole:noop,preselected:true});
  assert.ok(html.includes(`<b>${roleSet.defaultRole}</b>`)&&html.includes('(preselected; change or clear it before starting)'));
  assert.ok(html.includes('<b>No role</b>: product guidance only.'));
  // ROLE SL-1 (owner ruling 2026-10-10): TASK is not listed as a conversation role, only explained.
  assert.ok(!/value="TASK"/.test(html)&&!html.includes('<b>TASK</b>'),'TASK is not a choice');
  assert.equal((html.match(/name="start-thread-role"/g)??[]).length,4,'three conversation roles and No role, in the group the caller names');
  const trialGroup=h(RoleChoice,{group:'clean-trial-role:trial:7',roleSet,limits,role:'',setRole:noop,preselected:false});
  assert.equal((trialGroup.match(/name="clean-trial-role:trial:7"/g)??[]).length,4,'another instance, another group');
  assert.ok(!trialGroup.includes('name="start-thread-role"')&&!/name="conversation-role"/.test(html+trialGroup),'no shared hard-coded group');
  assert.ok(html.includes('TASK is not a conversation role: a manager assigns bounded work to it'));
  // The host's list governs when it is handed.
  const hostList=h(RoleChoice,{group:"start-thread-role",roleSet:{...roleSet,conversationRoles:['HELP_HUMAN','WORKING_ITEMS']},limits,role:'',setRole:noop,preselected:false});
  assert.ok(hostList.includes('value="WORKING_ITEMS"')&&!hostList.includes('value="HELPS_HUMANS"')&&!hostList.includes('value="TASK"'));
  const invalidList=h(RoleChoice,{group:"start-thread-role",roleSet:{...roleSet,conversationRoles:['HELP_HUMAN','TASK']},limits,role:'',setRole:noop,preselected:false});
  assert.ok(!invalidList.includes('value="TASK"'),'a malformed list cannot turn TASK into a primary conversation role');
  // Continue as offers the same three and No role, never TASK.
  const cont=header(thread());
  assert.ok(!/<option[^>]*value="TASK"/.test(cont)&&/<option[^>]*value="WORKING_ITEMS"/.test(cont));
  assert.ok(html.includes('Stated, not enforced'));
  assert.ok(!html.includes('"standing"'),'no JSON in the start display');
  const changed=h(RoleChoice,{group:"start-thread-role",roleSet,limits,role:'',setRole:noop,preselected:false});
  assert.ok(!changed.includes('(preselected'),'a cleared choice is no longer a preselection');
  // DEL-02-04 TBD-004 and exit criterion 3: the shipped set preselects HELP_HUMAN, as data.
  assert.equal(bundled.defaultRole,'HELP_HUMAN');
  assert.deepEqual(roles.filter(r=>r.default_for_new_chat).map(r=>r.name),['HELP_HUMAN']);
  const shipped=h(RoleChoice,{group:"start-thread-role",roleSet:bundled,limits,role:bundled.defaultRole,setRole:noop,preselected:true});
  assert.ok(/<input[^>]*checked=""[^>]*value="HELP_HUMAN"\/> <b>HELP_HUMAN<\/b>: Alignment with the human \(preselected; change or clear it before starting\)/.test(shipped),'the shipped default is shown preselected');
  assert.ok(shipped.includes('value=""')&&!/<input[^>]*checked=""[^>]*value=""\/>/.test(shipped),'No role is offered, to clear the preselection');
  const cleared=h(RoleChoice,{group:"start-thread-role",roleSet:bundled,limits,role:'',setRole:noop,preselected:false});
  assert.ok(!cleared.includes('(preselected')&&/<input[^>]*checked=""[^>]*value=""\/>/.test(cleared)&&cleared.includes('(the default for a new conversation)'),'cleared to No role, the default is only labelled');
  const noDefault={available:true,roles:roles.map(r=>({...r,default_for_new_chat:false})),defaultRole:null};
  const none=h(RoleChoice,{group:"start-thread-role",roleSet:noDefault,limits,role:noDefault.defaultRole??'',setRole:noop,preselected:false});
  assert.ok(!none.includes('(preselected')&&/<input[^>]*checked=""[^>]*value=""\/>/.test(none),'with no default in the set, No role is the start');
  const taskLimits=h(RoleLimits,{limits,role:'TASK'});
  assert.ok(taskLimits.includes('A task agent does not delegate: <b>Stated, not enforced</b>. It is stated in the role&#x27;s guidance; Codex does not enforce it. None of these enforces it either: your approval setting, your sandbox setting, your Codex configuration or your delegation depth limit.'));
  assert.ok(!/Not this limit|approval-policy|depth-limit|U-R6|U-R11/.test(html+taskLimits),'no engineering codes where a person meets the limits');
  const modified=h(RoleLimits,{limits:{...limits,account:{roles:[{role:'TASK',limits:[{...task,standing:'unknown',presentedAs:'Not known whether the supplied guidance states this'}]}]}},role:'TASK'});
  assert.ok(modified.includes('Not known whether the supplied guidance states this')&&!modified.includes('Stated, not enforced'));
  assert.ok(h(RoleLimits,{limits:{...limits,account:{roles:[]},notRead:[{role:'TASK',reason:'r',reading:'Limits not known'}]},role:'TASK'}).includes('Limits not known (r)'));
  const supply=h(SupplyStatus,{supply:{state:'response-observed',selection:'HELP_HUMAN',carried:{developerInstructions:{parts:[{source:{path:'AGENTS.md',state:'default'},length:10},{source:{path:'agents/AGENT_HELP_HUMAN.md',state:'modified'},length:5}]}}}});
  assert.ok(supply.includes('AGENTS.md (default, 10 bytes) + agents/AGENT_HELP_HUMAN.md (modified, 5 bytes)')&&supply.includes('Whether the model takes it up is unknown.'));
});

test('each conversation role is offered with a plain meaning from its shipped guidance, and its limits in plain words',()=>{
  // AC-001 "with their meanings": the line beside each role comes from its own shipped document.
  const doc=name=>readFileSync(new URL(`../src-tauri/resources/instructions/agents/AGENT_${name}.md`,import.meta.url),'utf8').replace(/\s+/g,' ');
  for (const [name,phrase] of [['HELP_HUMAN',"the person's intended outcome, commitments and work already in progress"],['HELPS_HUMANS','conceive and design workflows, tools and projects'],['WORKING_ITEMS','a bounded undertaking through implementation']]) {
    assert.ok(doc(name).includes(phrase),`${name}'s document carries the phrase its line is taken from`);
    const html=h(RoleChoice,{group:'g',roleSet,limits,role:name,setRole:noop,preselected:false});
    assert.ok(html.includes(ROLE_PLAIN_MEANING[name].replaceAll("'",'&#x27;')),`${name} shows its plain meaning`);
    // AC-003/AC-004 and V4-ROLE-03: the chosen role's limit is shown as stated, not enforced, with no enforcement implied.
    assert.ok(html.includes("Work within the brief&#x27;s write targets: <b>Stated, not enforced</b>. It is stated in the role&#x27;s guidance; Codex does not enforce it. None of these enforces it either: the brief itself, working in a separate worktree, your sandbox setting or your approval setting."),`${name}'s limit in plain words`);
    assert.ok(!/Enforced by Codex|Not this limit|brief-text|approval-policy/.test(html));
    assert.ok(html.includes('Codex does not enforce them, and your approval and sandbox settings are a separate matter that does not enforce them either.'));
  }
  assert.equal(ROLE_PLAIN_MEANING.TASK,undefined,'TASK is not offered, so it has no start line');
  // A limit whose standing is unknown keeps its unknown label and claims no enforcement.
  assert.equal(limitWords({...task,standing:'unknown',presentedAs:'Not known whether the supplied guidance states this'}),'None of these enforces it: your approval setting, your sandbox setting, your Codex configuration or your delegation depth limit.');
  // The general note is never shown over a limit Codex enforces.
  const enforced={...limits,account:{roles:[{role:'HELP_HUMAN',limits:[{...all,standing:'enforced-by-supplier',presentedAs:'Enforced by Codex',mechanism:'a named control'}]}]}};
  const withEnforced=h(RoleChoice,{group:'g',roleSet,limits:enforced,role:'HELP_HUMAN',setRole:noop,preselected:false});
  assert.ok(withEnforced.includes('<b>Enforced by Codex</b>. Codex enforces it through a named control.')&&!withEnforced.includes('Codex does not enforce'));
  // The start display carries no engineering status line for the role set.
  const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
  assert.ok(!app.includes('Role set: {host?.roleSet?.standing'));
  assert.ok(app.includes('preselected: !roleTouched && !!role && role === source?.roleSet?.defaultRole'),'the start records preselected against chosen');
});

test('Continue as offers the roles with their meanings and shows the chosen role\'s limits',()=>{
  const html=header(thread());
  assert.ok(html.includes('<option value="HELPS_HUMANS">HELPS_HUMANS: Design</option>')&&html.includes('<option value="WORKING_ITEMS">WORKING_ITEMS: Managed execution</option>'));
  assert.ok(html.includes('<option value="">No role: product guidance only</option>')&&!/<option[^>]*value="TASK"/.test(html));
  // The current role's limits show once; another target is shown only when chosen (state is the select's).
  assert.equal((html.match(/aria-label="Limits of HELP_HUMAN"/g)??[]).length,1);
  const fromWorking=header(thread({appRole:{standing:'app-observed',role:'WORKING_ITEMS',supply_ref:'sup:2'}}));
  assert.equal((fromWorking.match(/aria-label="Limits of WORKING_ITEMS"/g)??[]).length,1);
  const unknownRole=header(thread({appRole:{standing:'unknown',reason:'r'}}));
  assert.ok(unknownRole.includes('HELP_HUMAN: '+ROLE_PLAIN_MEANING.HELP_HUMAN.replaceAll("'",'&#x27;'))&&unknownRole.includes('aria-label="Limits of HELP_HUMAN"'),'a target other than the own role shows its meaning and limits');
});

test('Continue as: an editable unsent draft, no model chosen, nothing sent until the person sends',()=>{
  const handoff={id:'continue-as:1',sourceThread:'thread',sourceRoleLabel:'role HELP_HUMAN',targetRole:'WORKING_ITEMS',requestText:'Please draft a handoff summary…',request:{state:'sent',turnId:'turn-1'},
    header:'Handoff from conversation thread (role HELP_HUMAN).',draft:{state:'drafted',reading:'Drafted by the source conversation\'s agent in a visible turn there. Edit it before you send it.'},
    draftText:'Handoff from conversation thread (role HELP_HUMAN).\n\nThe summary.',started:null};
  const entries=[{value:'local-provider',label:'Configured local provider'}];
  const html=h(ContinueAsPanel,{handoff,entries,busy:false,ready:true,start:noop,send:noop,open:noop,dismiss:noop});
  assert.ok(html.includes('Handoff from conversation thread (role HELP_HUMAN).\n\nThe summary.</textarea>'));
  assert.ok(html.includes('it keeps its role'));
  assert.ok(html.includes('The new conversation starts with no model selected; choose how it connects and its model.')&&html.includes('Not started — no model selected.'));
  assert.ok(/<button disabled="">Start new conversation as WORKING_ITEMS<\/button>/.test(html),'no start without a model');
  assert.ok(!html.includes('Send this message'),'nothing can be sent before the new conversation exists');
  const started=h(ContinueAsPanel,{handoff:{...handoff,started:{threadId:'thread-2',generation:g}},entries,busy:false,ready:true,start:noop,send:noop,open:noop,dismiss:noop});
  assert.ok(started.includes('New conversation thread-2 started with WORKING_ITEMS. Nothing has been sent to it.'));
  assert.ok(started.includes('Send this message to the new conversation'));
  const fallback=h(ContinueAsPanel,{handoff:{...handoff,draft:{state:'header-only',reading:'The source turn ended failed. The draft holds the header only; write the summary yourself.'},draftText:handoff.header},entries,busy:false,ready:true,start:noop,send:noop,open:noop,dismiss:noop});
  assert.ok(fallback.includes('write the summary yourself')&&fallback.includes('(role HELP_HUMAN).</textarea>'));
  // While the summary is awaited the draft cannot be edited, so its arrival never replaces the person's edits.
  const textarea=html=>html.match(/<textarea[^>]*>/)[0];
  const waiting=h(ContinueAsPanel,{handoff:{...handoff,draft:{state:'waiting',reading:'Waiting for the source conversation\'s agent to finish the summary turn.'},draftText:handoff.header},entries,busy:false,ready:true,start:noop,send:noop,open:noop,dismiss:noop});
  assert.ok(textarea(waiting).includes('disabled=""'),'not editable while waiting');
  assert.ok(!textarea(html).includes('disabled=""')&&!textarea(fallback).includes('disabled=""'),'editable once drafted or header-only');
});

test('the existing boolean send helper preserves its result and refusal presentation',async()=>{
  assert.deepEqual(await attemptSend(async()=>true,'hello'),{state:'sent'});
  assert.equal((await attemptSend(async()=>false,'hello')).state,'failed');
  const thrown=await attemptSend(async()=>{throw new Error('refused-not-sent(not-ready)');},'hello');
  assert.equal(thrown.state,'failed');
  assert.ok(thrown.failure.includes('refused-not-sent(not-ready)'));
  const failedLine=h(SendOutcome,{outcome:thrown});
  assert.ok(failedLine.includes('Not sent: Error: refused-not-sent(not-ready)')&&failedLine.includes('The draft is kept; nothing is resent automatically.'));
  assert.ok(!failedLine.includes('Sent once'),'a refused send is never reported as sent');
  assert.ok(h(SendOutcome,{outcome:{state:'sent'}}).includes('Sent once as an ordinary message'));
  assert.equal(h(SendOutcome,{outcome:{state:'unsent'}}),'');
  // Continue-as now consumes the native owner's distinct outcomes. Its mounted
  // App/producer join is checked in continue-as-send.test.mjs; this helper's
  // existing boolean contract remains unchanged.
});

test('model and provider are exact strings: no capitalisation, autocorrect, spell-check or autofill (witness D-2)',()=>{
  const inputs=html=>html.match(/<input[^>]*>/g)??[];
  const exact=tag=>tag.includes('autoCapitalize="off"')&&tag.includes('autoCorrect="off"')&&tag.includes('spellCheck="false"')&&tag.includes('autoComplete="off"');
  const pair=inputs(h(ModelProviderFields,{model:'gpt-6-luna',modelProvider:'openai',setModel:noop,setModelProvider:noop}));
  assert.equal(pair.length,2);
  assert.ok(pair[0].includes('value="gpt-6-luna"')&&pair[1].includes('value="openai"'));
  assert.ok(pair.every(exact),pair.join('\n'));
  // Continue as asks for the new conversation's model and provider through the same fields.
  const handoff={id:'continue-as:1',sourceThread:'thread',sourceRoleLabel:'no role',targetRole:'HELPS_HUMANS',requestText:'r',request:{state:'sent'},draft:{state:'drafted',reading:'d'},draftText:'t',started:null};
  const panel=inputs(h(ContinueAsPanel,{handoff,entries:[],busy:false,ready:true,start:noop,send:noop,open:noop,dismiss:noop}));
  assert.equal(panel.length,2);
  assert.ok(panel.every(exact),panel.join('\n'));
  // The start display uses the same fields; no other model or provider input exists.
  // In the App, the start display's model and provider fields are exercised in
  // conversation-panel.test.mjs; Continue as uses them in trial-continue-model-choice.
});

test('the header shows the host’s trial header and the trials started here (TT-3b, TT-4)',()=>{
  const {TrialHeader}=load('ConversationRoles.tsx');
  const clean={threadId:'thread',reference:'trial:5',sequence:2,draftName:'load-check',rev12:'0123456789ab',header:'Trial 2 of draft load-check at content 0123456789ab — not registered; not a workflow run · authoring conversation auth',fork:false};
  const html=h(RoleHeader,{thread:thread(),limits,busy:false,ready:true,continueAs:noop,fork:noop,trialConversation:clean});
  assert.ok(html.includes('<b>Trial 2 of draft load-check at content 0123456789ab — not registered; not a workflow run · authoring conversation auth</b>'));
  const started=h(RoleHeader,{thread:thread(),limits,busy:false,ready:true,continueAs:noop,fork:noop,trialsStartedHere:{threadId:'thread',trials:[{reference:'trial:5',sequence:2,draftName:'load-check',kind:'clean'},{reference:'trial:6',sequence:3,draftName:'load-check',kind:'delegated'}]}});
  assert.ok(started.includes('Trials started here: trial 2 of draft load-check (clean); trial 3 of draft load-check (delegated).'));
  assert.ok(!header(thread()).includes('Trial header'),'no trial line for an ordinary conversation');
  assert.equal(h(TrialHeader,{}),'');
});

test('cold supply history is quoted with source bytes and limits, never current role authority',()=>{
  const {RoleSupplyHistory}=load('ConversationRoles.tsx');
  const view={standing:'Quoted App observations; mutable provenance unverified',limits:['unfinished import'],observations:[{record:{trigger:'thread-start',outcome:'supplied',supplyId:'sup:old',adoption:'unknown'},sourceBytes:{composed:'<do not execute>\r\n',parts:[{source:{path:'AGENTS.md'},kind:'product-guidance',text:'Old exact common'}]},limits:['source claim unverified']}]};
  const html=h(RoleSupplyHistory,{view});assert.ok(html.includes('Quoted App role-supply history'));assert.ok(html.includes('unfinished import')&&html.includes('source claim unverified'));assert.ok(html.includes('&lt;do not execute&gt;'));assert.ok(html.includes('Old exact common'));assert.ok(html.includes('does not set the conversation&#x27;s role or restore CCE authority'));assert.ok(html.includes('Supplier adoption remains unknown'));
  const headerHtml=header(thread({appRole:{standing:'unknown',reason:'original App supply binding not established'}}));assert.ok(headerHtml.includes('Role not established in this App process'));assert.ok(!headerHtml.includes('Role: <b>HELP_HUMAN</b>'));
});
test('unavailable or empty quoted history keeps visible limits and bytes unknown',()=>{
  const {RoleSupplyHistory}=load('ConversationRoles.tsx');const html=h(RoleSupplyHistory,{view:{limits:['store unavailable; history incomplete'],observations:[]}});assert.ok(html.includes('store unavailable; history incomplete'));assert.ok(html.includes('No role-supply observations were returned. The limits above apply.'));
  const old=h(RoleSupplyHistory,{view:{observations:[{record:{trigger:'fork',outcome:'unknown'},sourceBytes:null,limits:['source supply reference missing']}]}});assert.ok(old.includes('source supply reference missing'));assert.ok(old.includes('Exact App instruction bytes are not established'));
  const supply=h(SupplyStatus,{supply:{state:'response-observed',roleSupplyRecord:{state:'not-confirmed',limit:'flush unknown'}}});assert.ok(supply.includes('Role-supply history was not confirmed: flush unknown'));assert.ok(supply.includes('Native effects remain as observed; nothing is resent'));
});

test('an old pending source read cannot populate a new home or conversation scope',async()=>{
  let cursor=0;const slots=[];let effectScope;let cleanup;
  const hooks={useState(initial){const index=cursor++;if(!(index in slots))slots[index]=initial;return [slots[index],value=>{slots[index]=value;}];},useRef(initial){const index=cursor++;if(!(index in slots))slots[index]={current:initial};return slots[index];},useEffect(effect,deps){cursor++;if(effectScope!==deps[0]){cleanup?.();effectScope=deps[0];cleanup=effect();}}};
  const url=new URL('../src/ConversationRoles.tsx',import.meta.url);const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});const exports={};const real=localRequire(createRequire(url));new Function('require','exports',compiled.outputText)(name=>name==='react'?hooks:real(name),exports);
  let finish;const old=new Promise(resolve=>{finish=resolve;});const render=props=>{cursor=0;return exports.RoleHistoryReader(props);};
  const first=render({scope:'homeA/thread/counter1',ready:true,read:()=>old});first.props.children[0].props.onClick();assert.equal(slots[1],true);
  const current=render({scope:'homeB/thread/counter2',ready:true,read:async()=>({observations:[{record:{supplyId:'sup:current'}}]})});finish({observations:[{record:{supplyId:'sup:old'}}]});await new Promise(resolve=>setImmediate(resolve));assert.equal(slots[0],null);assert.equal(slots[1],false);
  current.props.children[0].props.onClick();await new Promise(resolve=>setImmediate(resolve));assert.equal(slots[0].observations[0].record.supplyId,'sup:current');cleanup?.();
});

test('late source-bound supply is shown separately from the original wait, never borrowed from another start',()=>{
  const carried={baseInstructions:'not-set',developerInstructions:{content:{method:'chirality.app.exact-bytes.sha256/v1',value:'a'.repeat(64)},byteLength:15,parts:[{source:{path:'AGENTS.md',state:'default'},length:10},{source:{path:'agents/AGENT_HELP_HUMAN.md',state:'modified'},length:5}]}};
  const roleSet={method:'chirality.app.exact-bytes.sha256/v1',value:'b'.repeat(64)};
  const fixture={state:'start-failed-or-unknown',supplyRef:'sup:late',selection:'HELP_HUMAN',generation:g,carried,roleSet,originalStartReceipts:[{supplyRef:'sup:late',selection:'HELP_HUMAN',generation:structuredClone(g),carried:structuredClone(carried),roleSet:structuredClone(roleSet),requestRef:'actual-private-receipt-fixture',requestIdentity:201,activeAdmission:true,writeResult:'written',outcome:'response-observed-result'}]};
  // The optional packet comes from the maintained actual Host→tick test's
  // ROLE_LATE_DTO output. CI also checks the same join shape without requiring
  // an external run artifact; neither packet changes live role authority.
  const supply=process.env.CHIRALITY_ROLE_LATE_PACKET?JSON.parse(readFileSync(process.env.CHIRALITY_ROLE_LATE_PACKET,'utf8')):fixture;
  const rendered=h(SupplyStatus,{supply});
  assert.ok(rendered.includes('Last start call: start-failed-or-unknown'));
  assert.ok(rendered.includes('Supplied at start (retained original receipt)'));
  assert.ok(!rendered.includes('native supply not established'));
  assert.ok(rendered.includes('Whether the model takes it up is unknown.'));
  for(const change of [r=>{r.supplyRef+='-foreign';},r=>{r.selection='WORKING_ITEMS';},r=>{r.generation.spawnCounter++;},r=>{r.carried.developerInstructions.content.value='0'.repeat(64);},r=>{r.roleSet.value='0'.repeat(64);},r=>{r.activeAdmission=false;},r=>{r.writeResult='write-failed';},r=>{r.outcome='response-observed-error';},r=>{delete r.requestRef;}]){
    const wrong=structuredClone(supply);change(wrong.originalStartReceipts[0]);const html=h(SupplyStatus,{supply:wrong});
    assert.ok(html.includes('Prepared App guidance; native supply not established by a matching retained receipt'));
    assert.ok(!html.includes('Supplied at start (retained original receipt)'));
  }
  const prepared=structuredClone(supply);prepared.state='response-observed';prepared.originalStartReceipts=[];
  assert.ok(!h(SupplyStatus,{supply:prepared}).includes('Supplied at start'));
});

const identity=letter=>({method:'chirality.app.exact-bytes.sha256/v1',value:letter.repeat(64)});
const nativeChild=(role='TASK')=>({role,status:'supplied',configKeys:[`agents.${role}.description`,`agents.${role}.config_file`],composed:identity('c'),file:identity('d')});
function childSupply(selection='HELP_HUMAN') {
  const offered=selection==='HELP_HUMAN'?['HELPS_HUMANS','WORKING_ITEMS','TASK']:['HELPS_HUMANS','WORKING_ITEMS'].includes(selection)?['TASK']:[];
  const carried={baseInstructions:'not-set',developerInstructions:{content:identity('a'),byteLength:10,parts:[{source:{path:'AGENTS.md',state:'default'},length:10}]},nativeChildRoles:roles.map(r=>offered.includes(r.name)?nativeChild(r.name):{role:r.name,status:'not-supplied',reason:'not-offered-by-role'})};
  const supply={state:'response-observed',supplyRef:'sup:parent',selection,generation:g,roleSet:identity('b'),carried,
    childNamespaceObservation:{standing:'observed configuration and source bytes; not a lock on later changes',candidateNames:['PERSON_ROLE'],sourceCount:4,config:identity('e')}};
  supply.originalStartReceipts=[{supplyRef:supply.supplyRef,selection,generation:structuredClone(g),roleSet:structuredClone(supply.roleSet),carried:structuredClone(carried),requestRef:'req:start',requestIdentity:201,activeAdmission:true,writeResult:'written',outcome:'response-observed-result'}];
  return supply;
}

test('child catalog presents the host matrix without adding TASK to primary roles',()=>{
  for (const [selection,count] of [['HELP_HUMAN',3],['HELPS_HUMANS',1],['WORKING_ITEMS',1],[null,0]]) {
    const supply=childSupply(selection);
    const html=h(NativeChildRoles,{supply});
    assert.equal((html.match(/Supplied in the original parent start\./g)??[]).length,count);
    assert.equal((html.match(/Not supplied\. Not offered by this conversation&#x27;s role\./g)??[]).length,4-count);
    assert.ok(html.includes('PERSON_ROLE')&&html.includes('Sources observed: 4')&&html.includes(identity('e').value));
    assert.ok(html.includes('not a lock on later changes'));
    assert.ok(html.includes('TASK&#x27;s guidance says a task agent does not delegate; that limit is stated, not enforced: Codex does not enforce it.'));
    assert.ok(!/<(input|option|button)/.test(html),'catalog is evidence, with no role-changing or delegation control');
    assert.ok(h(SupplyStatus,{supply}).includes('aria-label="Native child role supply"'),'the ordinary supply display consumes the catalog');
  }
});

test('child role supply requires the complete original receipt, including child bytes and file identity',()=>{
  const supply=childSupply();
  for (const change of [s=>{s.originalStartReceipts=[];},s=>{s.originalStartReceipts[0].carried.nativeChildRoles.find(r=>r.status==='supplied').file.value='f'.repeat(64);},s=>{s.originalStartReceipts[0].carried.nativeChildRoles.find(r=>r.status==='supplied').composed.value='f'.repeat(64);},s=>{s.originalStartReceipts[0].generation.spawnCounter++;},s=>{s.originalStartReceipts[0].roleSet=identity('f');},s=>{s.originalStartReceipts[0].activeAdmission=false;},s=>{s.originalStartReceipts[0].writeResult='write-failed';},s=>{s.originalStartReceipts[0].outcome='response-observed-error';},s=>{delete s.originalStartReceipts[0].requestRef;}]) {
    const prepared=structuredClone(supply);change(prepared);
    const html=h(NativeChildRoles,{supply:prepared});
    assert.equal((html.match(/Prepared; native supply not established\./g)??[]).length,3);
    assert.ok(!html.includes('Supplied in the original parent start.'));
  }
  // A later call failure does not erase a matched original successful receipt.
  assert.ok(h(NativeChildRoles,{supply:{...supply,state:'start-failed-or-unknown'}}).includes('Supplied in the original parent start.'));
  assert.equal(h(NativeChildRoles,{supply:{nativeChildRoles:[nativeChild()]}}),'','an unbound top-level status is not a carrier');
});

test('withheld child roles explain collisions, unreadable sources, unestablished support and publication failure',()=>{
  const reasons=['user-configuration-defines-role','user-configuration-not-read','mechanism-not-supported-at-pin','child-guidance-unavailable','child-file-unavailable','future-withholding-reason'];
  const supply=childSupply();supply.carried.nativeChildRoles=reasons.map(reason=>({role:'TASK',status:'not-supplied',reason}));
  supply.childNamespaceObservation={standing:'Native child roles withheld: configuration origins or source currency unavailable'};
  const html=h(NativeChildRoles,{supply});
  for (const reading of ['A person-defined role with this name was preserved.','Configuration origins or source currency could not be established.','Child-role carrier support is not established for this acting supplier.','Child guidance could not be read or composed.','The App child guidance file could not be published or verified.','future-withholding-reason']) assert.ok(html.includes(reading),reading);
  assert.equal((html.match(/Not supplied\./g)??[]).length,reasons.length);
  assert.ok(!html.includes('Supplied in the original parent start.')&&!html.includes('Sources observed:'));
  assert.ok(html.includes('The App leaves your own roles, features, delegation depth and permissions as they are.'));
});

test('unknown or different acting supplier identity withholds support without claiming version incompatibility',()=>{
  // Core uses this reason when executable identity is unknown or different,
  // even with a compatible declared version and configuration. The UI receives
  // the withholding reason; it must not turn it into a version-level conclusion.
  const supply=childSupply();supply.originalStartReceipts=[];
  supply.carried.nativeChildRoles=supply.carried.nativeChildRoles.map(child=>child.status==='supplied'?{role:child.role,status:'not-supplied',reason:'mechanism-not-supported-at-pin'}:child);
  const html=h(SupplyStatus,{supply});
  assert.ok(html.includes('Child-role carrier support is not established for this acting supplier.'));
  assert.ok(!html.includes('This Codex version does not support'));
  assert.ok(!html.includes('Supplied in the original parent start.'));
});

const childEvent={generation:g,parentThreadId:'parent',threadId:'child',turnId:'turn:1',itemId:'native-item:1',receiptPosition:17,source:'live item/completed subAgentActivity(kind=started)'};
const associatedChild={standing:'app-observed-child-supply',role:'TASK',parentSupplyRef:'sup:parent',composition:identity('c'),file:identity('d'),native:childEvent,metadataRequestRef:'req:metadata',agentRole:'TASK',parentThreadId:'parent',limitAccount:{role:'TASK',limits:[task,all]},providerAdoption:'unknown',currentRoleAuthorityRestored:false,basis:'original parent + native event + metadata',roleSupplyRecord:{state:'written'}};

test('selected child evidence remains historical and separate from the primary conversation role',()=>{
  const html=header(thread({threadId:'child',appRole:{standing:'unknown',reason:'no primary App binding'},childGuidance:associatedChild}));
  assert.ok(html.includes('Role not established in this App process (no primary App binding)'));
  assert.ok(html.includes('Original App child guidance: <b>TASK</b> (observed). Parent conversation: parent. Provider uptake remains unknown.'));
  assert.ok(!html.includes('Role: <b>TASK</b>')&&!/<option[^>]*value="TASK"/.test(html));
  assert.ok(html.includes('A task agent does not delegate: <b>Stated, not enforced</b>'));
  assert.ok(html.includes('It does not set the primary conversation role or restore current role authority'));
  assert.ok(html.includes('Resume, fork and later generations do not authorize new child associations from this catalog'));
  assert.ok(html.includes('req:metadata')&&html.includes('native-item:1')&&html.includes(identity('d').value),'original identity remains inspectable');
  const later=header(thread({generation:{...g,spawnCounter:2},threadId:'child',childGuidance:associatedChild}));
  assert.ok(later.includes('Original App child guidance')&&later.includes('&quot;spawnCounter&quot;: 1'),'later generations preserve the original evidence');
  const unknown=h(ChildAssociations,{associations:[{native:childEvent,guidance:{standing:'unknown',reason:'native child metadata pending'}}]});
  assert.ok(unknown.includes('Child child · parent parent · guidance unknown')&&unknown.includes('Child guidance unknown: native child metadata pending'));
  assert.ok(!unknown.includes('Original App child guidance')&&!unknown.includes('Stated, not enforced'));
  assert.ok(h(SupplyStatus,{supply:{childAssociations:[{native:childEvent,guidance:associatedChild}]}}).includes('Observed native children'),'events remain visible even when there is no last-start state');
});

test('TASK delegation shows the observed event, original standing and root provenance without enforcement claims',()=>{
  const observed={...childEvent,parentThreadId:'child',threadId:'grandchild',itemId:'native-item:2',receiptPosition:21,root:childEvent,parentSupplyRef:'sup:parent',standing:'stated-not-enforced',originalRole:'TASK',basis:'comparison-with-original-child-guidance',actionGeneration:g,originalAssociation:{associationId:'sup:child:1',generation:g,parentSupplyRef:'sup:parent',role:'TASK'}};
  const html=h(RoleLimitObservations,{observations:[observed]});
  const unknownDelegation=()=>h(RoleLimitObservations,{observations:[{...observed,standing:'unknown'}]});
  assert.ok(html.includes('Child child started child grandchild. The TASK guidance it was given says a task agent does not delegate: <b>Stated, not enforced</b>.'));
  assert.ok(html.includes('Delegations by an agent given TASK guidance'));
  assert.ok(html.includes('Codex does not enforce this limit. The App recorded this delegation and did not prevent it.'));
  assert.ok(!unknownDelegation().includes('Codex does not enforce this limit')&&unknownDelegation().includes('The App recorded this delegation and did not prevent it.'),'an unknown standing claims nothing about enforcement');
  assert.ok(html.includes('native-item:2')&&html.includes('receipt position 21')&&html.includes('Original root parent: parent · original parent supply: sup:parent'));
  assert.ok(html.includes('original TASK association: sup:child:1')&&!html.includes('Original guidance generation:'),'same-generation comparison keeps generation detail in raw evidence');
  const unknown=h(RoleLimitObservations,{observations:[{...observed,standing:'unknown',presentedAs:'TASK prohibition stated, not enforced'}]});
  assert.ok(unknown.includes('<b>Not known whether the supplied guidance states this</b>')&&!unknown.includes('<b>Stated, not enforced</b>'),'a modified original limit is not relabeled as default guidance');
  assert.ok(header(thread({roleLimitObservations:[observed]})).includes('aria-label="Observed TASK delegations"'),'shown in the source conversation');
  assert.ok(h(SupplyStatus,{supply:{roleLimitObservations:[observed]}}).includes('Delegations by an agent given TASK guidance'),'shown in the home supply display');
});

test('later native action compares with original TASK guidance without renewed supply or a new child association',()=>{
  const later={...g,spawnCounter:2};
  const event={...childEvent,generation:later,parentThreadId:'child',threadId:'grandchild',itemId:'native-item:later',receiptPosition:23};
  const observed={...event,root:childEvent,parentSupplyRef:'sup:parent',standing:'unknown',presentedAs:'Original TASK limit assessment unknown',originalRole:'TASK',basis:'comparison-with-original-child-guidance',actionGeneration:later,originalAssociation:{associationId:'sup:child:1',generation:g,parentSupplyRef:'sup:parent',role:'TASK'},comparisonStanding:'Original App guidance compared with a later native action; no renewed supply, provider uptake, RoleBinding, CCE or current-source authority'};
  const html=h(SupplyStatus,{supply:{childAssociations:[{native:childEvent,guidance:associatedChild},{native:event,guidance:{standing:'unknown',reason:'no supported original App parent carrier'}}],roleLimitObservations:[observed]}});
  assert.ok(html.includes(`Original guidance generation: ${JSON.stringify(g).replaceAll('"','&quot;')}. Native action generation: ${JSON.stringify(later).replaceAll('"','&quot;')}.`));
  assert.ok(html.includes('original TASK association: sup:child:1')&&html.includes('original parent supply: sup:parent'));
  assert.ok(html.includes('<b>Not known whether the supplied guidance states this</b>'),'edited original guidance keeps its unknown assessment');
  assert.ok(html.includes('It does not show that guidance was sent again, that the model took it up, or that the role still applies.'));
  assert.ok(html.includes('Child grandchild · parent child · guidance unknown'));
  assert.ok(html.includes('Child guidance unknown: no supported original App parent carrier.'));
  assert.equal((html.match(/Original App child guidance:/g)??[]).length,1,'only the original child has an association');
  assert.ok(!html.includes('TASK child child started')&&!html.includes('Supplied in the original parent start.'));
});

test('quoted history exposes exact child composition, sources, envelope and original limits without restoring associations',()=>{
  const {RoleSupplyHistory}=load('ConversationRoles.tsx');
  const child={role:'TASK',composed:'common\r\n\n# Active role: TASK\n\n<child instructions>',parts:[{source:{path:'agents/AGENT_TASK.md'},kind:'role-guidance',text:'<child instructions>'}],envelope:'developer_instructions = "quoted\\r\\n"\n',limitAccount:{role:'TASK',limits:[task]}};
  const html=h(RoleSupplyHistory,{view:{observations:[{record:{trigger:'thread-start',outcome:'supplied',supplyId:'sup:old'},sourceBytes:{composed:'original parent',parts:[],nativeChildren:[child]}}]}});
  assert.ok(html.includes('Recorded TASK child instruction bytes (quoted evidence)'));
  assert.ok(html.includes('common\r\n\n# Active role: TASK\n\n&lt;child instructions&gt;'));
  assert.ok(html.includes('agents/AGENT_TASK.md · role-guidance')&&html.includes('&lt;child instructions&gt;'));
  assert.ok(html.includes('Recorded child configuration file bytes')&&html.includes('developer_instructions = &quot;quoted\\r\\n&quot;\n'));
  assert.ok(html.includes('Recorded child limit account')&&html.includes('L-TASK-1'));
  assert.ok(html.includes('Quoted child bytes do not restore child associations')&&!html.includes('Original App child guidance'));
});
