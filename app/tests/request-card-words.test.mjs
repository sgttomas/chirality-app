import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {localRequire} from './support/load-src.mjs';

// DEL-01-04 REQ-001/AC-001: a tool-permission card says what each answer lets
// Codex do. Invented material only; the command request below has the shape
// of the pinned 0.167.0 ST-5 recording at position 13 (accept, a rule, cancel).
const load=(name,local={})=>{
  const url=new URL(`../src/${name}.tsx`,import.meta.url);
  const compiled=ts.transpileModule(readFileSync(url,'utf8'),{compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2022,jsx:ts.JsxEmit.ReactJSX}});
  const exports={};const base=createRequire(url);
  new Function('require','exports',compiled.outputText)(spec=>local[spec]??localRequire(base)(spec),exports);return exports;
};
const activity=load('NativeActivity');
const {NativeRequestCard,requestPlace,resolvePath,conversationPermissionWords}=load('RequestCards',{'./NativeActivity':activity});

const g={appSession:'s',home:'h',spawnCounter:1};
const at={threadId:'T',turnId:'u',itemId:'i'};
const request=(method,parameters)=>({recordKind:'server-request-entry',requestIdentity:method,generation:g,method,classification:'known-answerable',originClass:'a14',
  nativeParameters:{...at,...parameters},state:'outstanding',replyWriteResult:'not-attempted',acknowledgmentObservation:{status:'not-observed'}});
const fileChange=(params={})=>request('item/fileChange/requestApproval',{reason:'Write the invented marker',...params});
const viewWith=changes=>({home:g.home,generation:g,items:[{threadId:'T',turnId:'u',native:{id:'i',type:'fileChange',status:'inProgress',changes}}],turns:[],turnRecords:[],revisions:[],descendants:[]});
const change=(path,type='add',extra={})=>({path,kind:{type,...extra},diff:`+invented line for ${path}\n`});
// The recorded shape: item/commandExecution/requestApproval, ST-5 0.167.0 position 13, with an invented folder.
const recorded=()=>request('item/commandExecution/requestApproval',{kind:'command',environmentId:'local',reason:'Create the invented marker folder.',
  command:"/bin/zsh -lc 'mkdir st5-marker-pump-skid'",cwd:'/invented/pump-skid',commandActions:[{type:'unknown',command:'mkdir st5-marker-pump-skid'}],
  proposedExecpolicyAmendment:['mkdir','st5-marker-pump-skid'],
  availableDecisions:['accept',{acceptWithExecpolicyAmendment:{execpolicy_amendment:['mkdir','st5-marker-pump-skid']}},'cancel']});
const project={project:{kind:'folder',folder:'/invented/pump-skid'},conversationFolder:'/invented/pump-skid',permissionProfile:null};
const render=(r,view=null,place)=>renderToStaticMarkup(React.createElement(NativeRequestCard,{request:r,view,place,answer:async()=>{}}));
// The App's own words: everything except code spans, quoted supplier text and preformatted native content.
const appWords=html=>html.replace(/<pre[\s\S]*?<\/pre>/g,'').replace(/<code>[\s\S]*?<\/code>/g,'').replace(/<q>[\s\S]*?<\/q>/g,'').replace(/<[^>]+>/g,' ').replace(/&#x27;/g,"'");
const words=html=>appWords(html).replace(/\s+/g,' ');

test('a one-file change inside the project: count, full path, the part inside, an open diff and the location note',()=>{
  const html=render(fileChange(),viewWith([change('/invented/pump-skid/notes/README.md')]),project);
  assert.match(words(html),/Changes to 1 file:/);
  assert.match(html,/add <code>\/invented\/pump-skid\/notes\/README\.md<\/code> — in your project folder, at <code>notes\/README\.md<\/code>/);
  assert.doesNotMatch(html,/OUTSIDE/);
  assert.doesNotMatch(html,/<details><summary>add/,'the diff is not behind a closed disclosure');
  assert.match(html,/<pre style="[^"]*overflow:auto[^"]*">\+invented line for \/invented\/pump-skid\/notes\/README\.md/,'the diff is shown open in a scrollable box');
  assert.equal(html.split('Locations are read from the paths Codex gave; the App has not followed links.').length,2,'the location note appears once');
  assert.match(words(html),/If you allow this, Codex writes these files where they are shown, including any outside your project folder\./);
});

test('a two-file change with one file outside the project marks it OUTSIDE',()=>{
  const html=render(fileChange(),viewWith([change('/invented/pump-skid/a.txt','update'),change('/invented/elsewhere/b.txt','delete')]),project);
  assert.match(words(html),/Changes to 2 files:/);
  assert.match(html,/update <code>\/invented\/pump-skid\/a\.txt<\/code> — in your project folder, at <code>a\.txt<\/code>/);
  assert.match(html,/delete <code>\/invented\/elsewhere\/b\.txt<\/code> — OUTSIDE your project folder/);
  assert.doesNotMatch(html,/pump-skid-other/);
  // A sibling folder that shares the project folder's name as a prefix is outside it.
  assert.match(render(fileChange(),viewWith([change('/invented/pump-skid-old/c.txt')]),project),/— OUTSIDE your project folder/);
});

test('a relative path is resolved against the working folder; `..` that leaves the folder is OUTSIDE',()=>{
  const inside=render(fileChange(),viewWith([change('notes/./README.md')]),project);
  assert.match(inside,/add <code>\/invented\/pump-skid\/notes\/README\.md<\/code> \(relative to <code>\/invented\/pump-skid<\/code>\) — in your project folder, at <code>notes\/README\.md<\/code>/);
  const leaving=render(fileChange(),viewWith([change('../../outside/x.txt')]),project);
  assert.match(leaving,/<code>\/outside\/x\.txt<\/code> \(relative to <code>\/invented\/pump-skid<\/code>\) — OUTSIDE your project folder/);
  const absoluteDots=render(fileChange(),viewWith([change('/invented/pump-skid/sub/../../escape.txt')]),project);
  assert.match(absoluteDots,/<code>\/invented\/escape\.txt<\/code> — OUTSIDE your project folder/);
  assert.deepEqual(resolvePath('a/../../b',null),null,'a relative path with no working folder is not resolved');
  // A request's own cwd, when Codex gives one, is the working folder.
  assert.match(render(fileChange({cwd:'/invented/pump-skid/sub'}),viewWith([change('x.txt')]),project),/<code>\/invented\/pump-skid\/sub\/x\.txt<\/code> \(relative to <code>\/invented\/pump-skid\/sub<\/code>\) — in your project folder, at <code>sub\/x\.txt<\/code>/);
});

test('a conversation with no project measures against its working folder, in those words',()=>{
  const none={project:{kind:'none'},conversationFolder:'/invented/tmp/conversation-1',permissionProfile:null};
  const html=render(fileChange(),viewWith([change('/invented/tmp/conversation-1/x.txt'),change('/invented/pump-skid/y.txt')]),none);
  assert.match(html,/<code>\/invented\/tmp\/conversation-1\/x\.txt<\/code> — in this conversation’s working folder, at <code>x\.txt<\/code>/);
  assert.match(html,/<code>\/invented\/pump-skid\/y\.txt<\/code> — OUTSIDE this conversation’s working folder/);
  assert.match(words(html),/including any outside this conversation’s working folder\./);
  assert.doesNotMatch(words(html),/your project folder/);
});

test('the place comes from the host snapshot: project folder, no project, or not established',()=>{
  const r=fileChange();
  const threads=[{generation:g,threadId:'T',cwd:'/invented/tmp/conversation-1'},{generation:{...g,spawnCounter:2},threadId:'T',cwd:'/elsewhere'}];
  assert.deepEqual(requestPlace(r,{currentAppProjectContext:{reference:'/invented/pump-skid'},threads},'/invented/pump-skid'),{project:{kind:'folder',folder:'/invented/pump-skid'},conversationFolder:'/invented/tmp/conversation-1',permissionProfile:null});
  assert.deepEqual(requestPlace(r,{currentAppProjectContext:{reference:null},currentAppProjectContextLimit:null,threads},null).project,{kind:'none'});
  assert.deepEqual(requestPlace(r,{currentAppProjectContext:{reference:'/invented/pump-skid'},threads},null).project,{kind:'unknown'},'a project whose folder the App cannot display is not "no project"');
  assert.deepEqual(requestPlace(r,{},null),{project:{kind:'unknown'},conversationFolder:null,permissionProfile:null},'nothing read yet');
  const html=render(r,viewWith([change('/invented/a.txt')]),requestPlace(r,{},null));
  assert.doesNotMatch(html,/OUTSIDE|in your project folder, at/,'no mark is made without a folder to measure against');
  assert.match(words(html),/The App has not established where your project folder is/);
});

test('the list has not arrived: no count, the new sentence, and the answers stay offered',()=>{
  const html=render(fileChange(),null,project);
  assert.doesNotMatch(words(html),/Changes to/);
  assert.match(words(html),/The App has not received the list of files, so it cannot show where these changes go\. You can refuse, or wait for the list to appear, before allowing a change you cannot see\./);
  assert.doesNotMatch(words(html),/The changes are not shown here/);
  assert.doesNotMatch(words(html),/Codex writes these files where they are shown/);
  for(const value of ['accept','acceptForSession','decline','cancel']) assert.match(html,new RegExp(`<button>[^<]*<code>&quot;${value}&quot;</code></button>`),value);
});

test('the command card says the command runs outside the sandbox under a built-in profile, and with more access otherwise',()=>{
  const builtIn=words(render(recorded(),null,{...project,permissionProfile:':workspace'}));
  assert.match(builtIn,/If you allow this command, it runs once outside Codex’s sandbox, with your account’s access to all your files and to the network, in the working folder shown\./);
  for(const place of [{...project,permissionProfile:'engineering'},project,undefined]){
    const other=words(render(recorded(),null,place));
    assert.match(other,/If you allow this command, it runs once with more access than Codex’s sandbox gives, which may be all of your account’s access to your files and the network, in the working folder shown\./);
    assert.doesNotMatch(other,/runs once outside Codex’s sandbox/);
  }
});

test('the rule answer: its label and the line beside it, with the rule words',()=>{
  const html=render(recorded(),null,project);
  assert.match(html,/<button>Allow, and add a lasting rule \(see below\) <code>\{&quot;acceptWithExecpolicyAmendment&quot;/);
  assert.match(html,/<small> This adds a lasting rule to the rules file in this App’s sign-in folder: from then on, in every conversation of this home, any command beginning with <code>mkdir st5-marker-pump-skid<\/code> runs with more access than Codex’s sandbox gives, without asking\. It stays until it is removed from that file\.<\/small>/);
  assert.match(render(recorded(),null,{...project,permissionProfile:':read-only'}),/beginning with <code>mkdir st5-marker-pump-skid<\/code> runs outside Codex’s sandbox without asking\. It stays until it is removed from that file\./);
  // A bare rule value takes its words from the proposed rule.
  assert.match(render(request('item/commandExecution/requestApproval',{command:'ls',cwd:'/w',proposedExecpolicyAmendment:['ls','-la'],availableDecisions:['acceptWithExecpolicyAmendment','cancel']}),null,project),/beginning with <code>ls -la<\/code>/);
});

test('with no decline-type answer but cancel offered, the card says refusing interrupts the turn',()=>{
  const line=/Codex offers no way to refuse and let the agent continue: refusing interrupts the turn, and you can then tell the agent what to do instead\./;
  assert.match(words(render(recorded(),null,project)),line);
  assert.match(words(render(fileChange({availableDecisions:['accept','cancel']}),viewWith([change('/invented/pump-skid/a')]),project)),line);
  assert.doesNotMatch(words(render(request('item/commandExecution/requestApproval',{command:'ls',cwd:'/w'}),null,project)),line,'the default forms include decline');
});

test('"Allow for this session" says what it covers on both kinds of card',()=>{
  const files=render(fileChange(),viewWith([change('/invented/pump-skid/a')]),project);
  assert.match(files,/<button>Allow for this session <code>&quot;acceptForSession&quot;<\/code><\/button><small> Later changes to only these same files are not asked again until Codex stops\. Nothing is saved\.<\/small>/);
  const command=render(request('item/commandExecution/requestApproval',{command:'ls',cwd:'/w',availableDecisions:['accept','acceptForSession','decline','cancel']}),null,project);
  assert.match(command,/<button>Allow for this session <code>&quot;acceptForSession&quot;<\/code><\/button><small> This same command, in this folder, is not asked again until Codex stops\. Nothing is saved\.<\/small>/);
});

test('none of the words accept, approve or approval appear as the card’s own words',()=>{
  const cards=[
    render(recorded(),null,project),render(recorded(),null,{...project,permissionProfile:':workspace'}),
    render(fileChange(),viewWith([change('/invented/pump-skid/a'),change('/x/b')]),project),render(fileChange(),null,project),
    render(fileChange(),viewWith([change('/x/b')]),{project:{kind:'none'},conversationFolder:'/t',permissionProfile:null}),
    render(request('item/commandExecution/requestApproval',{command:'ls',cwd:'/w',availableDecisions:['accept','acceptForSession','decline','cancel']}),null,project),
  ];
  for(const html of cards) assert.doesNotMatch(appWords(html),/accept|approv/i,appWords(html));
});

// The profile Codex reported for the conversation reaches the card from the host's thread row; a
// built-in profile gives the certain words, anything else the cautious ones.
test('the reported permission profile comes from the conversation\'s row in the host snapshot',()=>{
  const r=fileChange();
  const threads=[{generation:g,threadId:'T',cwd:'/invented/pump-skid',activePermissionProfile:{id:':read-only'},sandbox:{type:'readOnly',networkAccess:false},approvalPolicy:'on-request'}];
  assert.equal(requestPlace(r,{currentAppProjectContext:{reference:'/invented/pump-skid'},threads},'/invented/pump-skid').permissionProfile,':read-only');
  assert.equal(requestPlace(r,{threads:[{...threads[0],activePermissionProfile:null}]},null).permissionProfile,null,'unreported stays null');
});
// What Codex may do in a conversation, as Codex reported it when the conversation started.
test('a conversation says what Codex reported it may do there, in the person\'s words, and says unreported as unreported',()=>{
  assert.equal(conversationPermissionWords({sandbox:{type:'readOnly',networkAccess:false},approvalPolicy:'on-request'}),
    'it can read files your account can read and change none without your permission (read-only); it asks you before doing more than that (on-request)');
  assert.equal(conversationPermissionWords({sandbox:{type:'workspaceWrite',networkAccess:true},approvalPolicy:'never'}),
    'it can read files your account can read and change files in its working folder without asking (workspace-write, with network); it never asks you (never)');
  assert.equal(conversationPermissionWords({sandbox:{type:'externalSandbox'},approvalPolicy:{granular:{}}}),
    'Codex reported its sandbox as externalSandbox; Codex reported its approval setting as {"granular":{}}');
  assert.equal(conversationPermissionWords({}),'Codex did not report its sandbox; Codex did not report when it asks you');
});
