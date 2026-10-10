import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
const load=name=>{const url=new URL(`../src/${name}`,import.meta.url);const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,jsx:ts.JsxEmit.ReactJSX}});const exports={};new Function('require','exports',compiled.outputText)(createRequire(url),exports);return exports;};
const {RoleHeader,RoleChoice,RoleLimits,ContinueAsPanel,SupplyStatus,guidanceChange,roleName,attemptSend,SendOutcome}=load('ConversationRoles.tsx');
const h=(c,p)=>renderToStaticMarkup(React.createElement(c,p));
const noop=()=>{};

const roles=JSON.parse(readFileSync(new URL('../src-tauri/resources/instructions/roles.json',import.meta.url),'utf8')).roles;
// The bundled set marks no default today (U-R11 is a release decision); a default is exercised with an invented copy.
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
  const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8')+readFileSync(new URL('../src/ConversationRoles.tsx',import.meta.url),'utf8');
  assert.ok(app.includes('"continue_as_begin"')&&app.includes('"conversation_fork"')&&app.includes('continueAs: handoff.id'));
  assert.ok(!/thread\/settings\/update|developer_instructions|setRole\(selected/.test(app));
});

test('the start display is readable: preselection, no role, TASK not offered, limits as handed',()=>{
  const html=h(RoleChoice,{roleSet,limits,role:roleSet.defaultRole,setRole:noop,preselected:true});
  assert.ok(html.includes(`<b>${roleSet.defaultRole}</b>`)&&html.includes('(preselected; change or clear it before starting)'));
  assert.ok(html.includes('<b>No role</b>: product guidance only.'));
  assert.ok(/<input[^>]*disabled=""[^>]*value="TASK"/.test(html)&&html.includes('Not offered as a conversation role here'));
  assert.ok(html.includes('Stated, not enforced'));
  assert.ok(!html.includes('"standing"'),'no JSON in the start display');
  const changed=h(RoleChoice,{roleSet,limits,role:'',setRole:noop,preselected:false});
  assert.ok(!changed.includes('(preselected'),'a cleared choice is no longer a preselection');
  const shipped=h(RoleChoice,{roleSet:bundled,limits,role:bundled.defaultRole??'',setRole:noop,preselected:false});
  assert.ok(!shipped.includes('(preselected')&&/<input[^>]*checked=""[^>]*value=""\/>/.test(shipped),'with no default in the set, No role is the start');
  const taskLimits=h(RoleLimits,{limits,role:'TASK'});
  assert.ok(taskLimits.includes('A task agent does not delegate: <b>Stated, not enforced</b>. Not this limit&#x27;s enforcement: approval-policy, sandbox, user-configuration, depth-limit.'));
  const modified=h(RoleLimits,{limits:{...limits,account:{roles:[{role:'TASK',limits:[{...task,standing:'unknown',presentedAs:'Not known whether the supplied guidance states this'}]}]}},role:'TASK'});
  assert.ok(modified.includes('Not known whether the supplied guidance states this')&&!modified.includes('Stated, not enforced'));
  assert.ok(h(RoleLimits,{limits:{...limits,account:{roles:[]},notRead:[{role:'TASK',reason:'r',reading:'Limits not known'}]},role:'TASK'}).includes('Limits not known (r)'));
  const supply=h(SupplyStatus,{supply:{state:'response-observed',selection:'HELP_HUMAN',carried:{developerInstructions:{parts:[{source:{path:'AGENTS.md',state:'default'},length:10},{source:{path:'agents/AGENT_HELP_HUMAN.md',state:'modified'},length:5}]}}}});
  assert.ok(supply.includes('AGENTS.md (default, 10 bytes) + agents/AGENT_HELP_HUMAN.md (modified, 5 bytes)')&&supply.includes('Whether the model takes it up is unknown.'));
});

test('Continue as: an editable unsent draft, no model chosen, nothing sent until the person sends',()=>{
  const handoff={id:'continue-as:1',sourceThread:'thread',sourceRoleLabel:'role HELP_HUMAN',targetRole:'WORKING_ITEMS',requestText:'Please draft a handoff summary…',request:{state:'sent',turnId:'turn-1'},
    header:'Handoff from conversation thread (role HELP_HUMAN).',draft:{state:'drafted',reading:'Drafted by the source conversation\'s agent in a visible turn there. Edit it before you send it.'},
    draftText:'Handoff from conversation thread (role HELP_HUMAN).\n\nThe summary.',started:null};
  const entries=[{value:'local-provider',label:'Configured local provider'}];
  const html=h(ContinueAsPanel,{handoff,entries,busy:false,ready:true,start:noop,send:noop,open:noop,dismiss:noop});
  assert.ok(html.includes('Handoff from conversation thread (role HELP_HUMAN).\n\nThe summary.</textarea>'));
  assert.ok(html.includes('it keeps its role'));
  assert.ok(html.includes('The new conversation starts with no model selected; choose one.')&&html.includes('Not started — no model selected.'));
  assert.ok(/<button disabled="">Start new conversation as WORKING_ITEMS<\/button>/.test(html),'no start without a model');
  assert.ok(!html.includes('Send this message'),'nothing can be sent before the new conversation exists');
  const started=h(ContinueAsPanel,{handoff:{...handoff,started:{threadId:'thread-2',generation:g}},entries,busy:false,ready:true,start:noop,send:noop,open:noop,dismiss:noop});
  assert.ok(started.includes('New conversation thread-2 started with WORKING_ITEMS. Nothing has been sent to it.'));
  assert.ok(started.includes('Send this message to the new conversation'));
  const fallback=h(ContinueAsPanel,{handoff:{...handoff,draft:{state:'header-only',reading:'The source turn ended failed. The draft holds the header only; write the summary yourself.'},draftText:handoff.header},entries,busy:false,ready:true,start:noop,send:noop,open:noop,dismiss:noop});
  assert.ok(fallback.includes('write the summary yourself')&&fallback.includes('(role HELP_HUMAN).</textarea>'));
});

test('the handoff message reads sent only after the send resolved; a refusal keeps the draft and allows another try',async()=>{
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
  // The panel takes its state from attemptSend's result, never before the send resolves.
  const source=readFileSync(new URL('../src/ConversationRoles.tsx',import.meta.url),'utf8');
  assert.ok(source.includes('void attemptSend(send, draft).then(setSending)')&&!/setSent\(true\)/.test(source));
  const app=readFileSync(new URL('../src/App.tsx',import.meta.url),'utf8');
  assert.ok(app.includes('mode: null })) !== undefined'),'the App reports a failed send as not sent');
});
