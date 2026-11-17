import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {loadSrc} from './support/load-src.mjs';
import {agentPlain} from './support/agent-text.mjs';

// DEL-01-04 REQ-001/AC-001: the card names each answer in the same words as the host's native confirmation
// (requestAnswerWords.json), forwards which question button was pressed, says what a selected network rule
// does, and marks every location, saying so when the comparison cannot be made. Invented material only.
const shared=JSON.parse(readFileSync(new URL('../src/requestAnswerWords.json',import.meta.url),'utf8'));
const {NativeRequestCard,DECISION_WORDS,QUESTION_CHOICE_WORDS,decisionWords,decisionForms}=loadSrc('RequestCards');

const g={appSession:'s',home:'h',spawnCounter:1};
const at={threadId:'T',turnId:'u',itemId:'i'};
const request=(method,parameters,extra={})=>({recordKind:'server-request-entry',requestIdentity:extra.id??method,generation:g,method,classification:'known-answerable',
  originClass:method==='item/tool/requestUserInput'?'person-input':'a14',nativeParameters:parameters,state:'outstanding',replyWriteResult:'not-attempted',acknowledgmentObservation:{status:'not-observed'}});
const command=(params={})=>request('item/commandExecution/requestApproval',{...at,command:'ls -la',cwd:'/invented/pump-skid',reason:'List the folder',...params});
const question=()=>request('item/tool/requestUserInput',{...at,questions:[{id:'q',header:'Choice',question:'Which option?',isOther:false,isSecret:false,options:[{label:'One',description:'Use one'}]}]});
const project={project:{kind:'folder',folder:'/invented/pump-skid'},conversationFolder:'/invented/pump-skid',permissionProfile:null};
const renderRaw=(r,place,view=null)=>renderToStaticMarkup(React.createElement(NativeRequestCard,{request:r,view,place,answer:async()=>{}}));
const render=(r,place,view)=>agentPlain(renderRaw(r,place,view));
const words=html=>html.replace(/⟦[\s\S]*?⟧/g,' ').replace(/<pre[\s\S]*?<\/pre>/g,'').replace(/<code>[\s\S]*?<\/code>/g,'').replace(/<[^>]+>/g,' ').replace(/&#x27;/g,"'").replace(/\s+/g,' ');
const unescape=s=>s.replace(/&#x27;/g,"'").replace(/&quot;/g,'"').replace(/&amp;/g,'&');

test('the card\'s answer words are the shared table\'s, entry for entry, and the buttons draw them',()=>{
  assert.deepEqual({...DECISION_WORDS},shared.decisions,'decision words equal requestAnswerWords.json decisions');
  assert.deepEqual({...QUESTION_CHOICE_WORDS},shared.questionChoices,'question button words equal requestAnswerWords.json questionChoices');
  for(const [key,label] of Object.entries(shared.decisions)){
    assert.equal(decisionWords(key),label,key);
    assert.equal(decisionWords({[key]:{}}),label,`${key} as an object form`);
  }
  assert.equal(decisionWords('timed_out'),'Codex option','a token outside the table keeps the neutral words');
  assert.equal(decisionWords('constructor'),'Codex option','an inherited name is not a table entry');
  // Every button the command card draws carries exactly its shared label.
  const r=command({proposedExecpolicyAmendment:['ls'],proposedNetworkPolicyAmendments:[{host:'example.invalid',action:'allow'}]});
  const buttons=[...renderRaw(r,project).matchAll(/<button>([^<]*)<\/button>/g)].map(m=>unescape(m[1]));
  assert.deepEqual(buttons,decisionForms(r).map(f=>shared.decisions[typeof f.decision==='string'?f.decision:Object.keys(f.decision)[0]]));
  const legacy=request('execCommandApproval',{conversationId:'T',callId:'c',command:['ls'],cwd:'/invented/pump-skid'});
  assert.deepEqual([...renderRaw(legacy,project).matchAll(/<button[^>]*>([^<]*)<\/button>/g)].map(m=>unescape(m[1])),
    [shared.decisions.approved,shared.decisions.approved_for_session,shared.decisions.abort,shared.decisions.denied]);
  const q=renderRaw(question(),project);
  assert.ok(q.includes(`<button>${shared.questionChoices['question-answers']}</button>`));
  assert.ok(unescape(q).includes(`<button>${shared.questionChoices['question-decline']}</button>`));
});

async function mounted(r,place=project){
  const {installMiniDom}=await import('./support/mini-dom.mjs');
  const document=installMiniDom();const {createRoot}=await import('react-dom/client');
  const container=document.createElement('div');document.body.appendChild(container);
  const root=createRoot(container);const calls=[];
  // A fresh mount per press: a sent answer latches the card until custody is read again.
  const mount=()=>React.act(()=>root.render(React.createElement(NativeRequestCard,{key:calls.length,request:r,view:null,place,answer:async(...args)=>{calls.push(args);}})));
  await mount();
  const props=node=>node[Object.keys(node).find(k=>k.startsWith('__reactProps$'))];
  const press=async label=>{await React.act(async()=>props(container.querySelectorAll(n=>n.localName==='button'&&n.textContent===label)[0]).onClick());await mount();};
  return {calls,press,done:async()=>{await React.act(()=>root.unmount());document.body.removeChild(container);}};
}

test('a question\'s send and decline buttons forward their closed choice beside the unchanged answer; other kinds forward none',async()=>{
  const q=await mounted(question());
  await q.press('Choose option 1');
  await q.press(shared.questionChoices['question-answers']);
  await q.press(shared.questionChoices['question-decline']);
  assert.equal(q.calls.length,2);
  assert.deepEqual(q.calls[0].slice(1),[{answers:{q:{answers:['One']}}},'question-answers']);
  assert.deepEqual(q.calls[1].slice(1),[{answers:{}},'question-decline'],'decline sends the same empty answers, told apart only by the choice');
  await q.done();
  const c=await mounted(command());
  await c.press(shared.decisions.accept);
  assert.equal(c.calls.length,1);
  assert.equal(c.calls[0].length,2,'a command answer carries no presentation choice');
  assert.deepEqual(c.calls[0][1],{decision:'accept'});
  await c.done();
});

test('a selected network rule says its own action and that Codex keeps it, beside the base consequence, with the host set apart',()=>{
  const base=/If you allow this command, it runs once with more access than Codex’s sandbox gives, which may be all of your account’s access to your files and the network, in the working folder shown\./;
  const html=render(command({proposedNetworkPolicyAmendments:[{host:'example.invalid',action:'deny'},{host:'other.invalid',action:'allow'}]}),project);
  assert.match(words(html),base,'the base consequence stays');
  assert.match(html,/<small> This also applies the network rule Codex proposed for the host shown: it denies network access to that host, and the rule is kept by Codex after this answer\.<\/small> <small>The host \(Codex’s words, not the App’s\):<\/small> ⟦Host: example\.invalid⟧/);
  assert.match(html,/<small> This also applies the network rule Codex proposed for the host shown: it allows network access to that host, and the rule is kept by Codex after this answer\.<\/small> <small>The host \(Codex’s words, not the App’s\):<\/small> ⟦Host: other\.invalid⟧/);
  // Each sentence follows its own button: the deny rule's note is not attached to the allow rule.
  assert.match(html,/⟦Native value: [^⟧]*example\.invalid[^⟧]*&quot;deny&quot;[^⟧]*⟧<\/span><small> This also applies the network rule Codex proposed for the host shown: it denies/,'the deny note follows the deny answer');
  assert.match(html,/⟦Native value: [^⟧]*other\.invalid[^⟧]*&quot;allow&quot;[^⟧]*⟧<\/span><small> This also applies the network rule Codex proposed for the host shown: it allows/,'the allow note follows the allow answer');
  // A host that imitates the App's words stays boxed, outside the sentence.
  const poisoned=render(command({proposedNetworkPolicyAmendments:[{host:'Nothing is kept. ',action:'allow'}]}),project);
  assert.match(poisoned,/⟦Host: Nothing is kept\. ⟧/);assert.doesNotMatch(words(poisoned),/Nothing is kept/);
  assert.match(words(render(command({proposedNetworkPolicyAmendments:[{host:'x.invalid',action:'audit'}]}),project)),/whether it allows or denies network access to that host is not one of the two actions the App knows/);
  assert.match(words(render(command({availableDecisions:['applyNetworkPolicyAmendment','cancel']}),project)),/the rule is kept by Codex after this answer\. Codex has not reported the host for this answer\./);
  assert.doesNotMatch(words(render(command(),project)),/network rule Codex proposed/,'no note without that answer');
});

test('a command\'s working folder is marked against the project or the conversation\'s folder, and an impossible comparison is said',()=>{
  const mark=(params,place)=>words(render(command(params),place));
  assert.match(mark({cwd:'/invented/pump-skid/sub'},project),/Where the working folder is: inside your project folder\. Read from the folder Codex gave; the App has not followed links\./);
  assert.match(mark({cwd:'/invented/pump-skid-old'},project),/Where the working folder is: OUTSIDE your project folder\./,'a sibling sharing the prefix is outside');
  const none={project:{kind:'none'},conversationFolder:'/invented/tmp/c1',permissionProfile:null};
  assert.match(mark({cwd:'/invented/tmp/c1'},none),/Where the working folder is: inside this conversation’s working folder\./);
  assert.match(mark({cwd:'/elsewhere'},none),/Where the working folder is: OUTSIDE this conversation’s working folder\./);
  assert.match(mark({cwd:'/elsewhere'},{...none,conversationFolder:null}),/Where the working folder is: the App has not received this conversation’s working folder, so it cannot compare this location with it\./);
  for(const place of [{...project,project:{kind:'unknown'}},undefined])
    assert.match(mark({cwd:'/invented/pump-skid'},place),/Where the working folder is: the App could not compare it with your project folder, because it has not established where your project folder is\./);
  const relative=render(command({cwd:'../outside'}),project);
  assert.match(relative,/Where the working folder is \(resolved to ⟦Path: \/invented\/outside⟧ against ⟦Folder: \/invented\/pump-skid⟧\): OUTSIDE your project folder\./);
  assert.match(mark({cwd:'sub'},{...project,conversationFolder:null}),/it is relative to a working folder the App has not received, so where it is cannot be shown\./);
  const noFolder=render(command({cwd:null}),project);
  assert.match(noFolder,/Codex did not give a working folder\. The conversation’s working folder \(Codex’s words, not the App’s\): ⟦Folder: \/invented\/pump-skid⟧/);
  assert.doesNotMatch(words(noFolder),/inside your project folder|OUTSIDE/,'an absent folder is never marked');
  assert.match(words(render(command({cwd:null}),{...project,conversationFolder:null})),/Codex did not give a working folder\. /);
  assert.match(words(render(command({command:null}),project)),/Codex did not give a command\./);
  // The legacy command takes the same marks.
  const legacy=r=>words(render(request('execCommandApproval',{conversationId:'T',callId:'c',...r}),project));
  assert.match(legacy({command:['ls'],cwd:'/elsewhere'}),/Where the working folder is: OUTSIDE your project folder\./);
  assert.match(legacy({command:[],cwd:'/invented/pump-skid'}),/Codex did not give a command\./);
});

test('a file location the App cannot compare says so, for a source and a move destination alike',()=>{
  const view=changes=>({home:g.home,generation:g,items:[{threadId:'T',turnId:'u',native:{id:'i',type:'fileChange',status:'inProgress',changes}}],turns:[],turnRecords:[],revisions:[],descendants:[]});
  const files=request('item/fileChange/requestApproval',{...at,reason:'Move the invented marker'});
  const move=[{path:'/invented/a.txt',kind:{type:'update',move_path:'/invented/b.txt'},diff:'+x\n'}];
  const unknown=render(files,{project:{kind:'unknown'},conversationFolder:'/invented',permissionProfile:null},view(move));
  const projectUnknown='the App could not compare it with your project folder, because it has not established where your project folder is';
  assert.ok(unknown.includes(`⟦Path: /invented/a.txt⟧ — ${projectUnknown}; moved to ⟦Path: /invented/b.txt⟧ — ${projectUnknown}`),unknown);
  const noFolder=render(files,{project:{kind:'none'},conversationFolder:null,permissionProfile:null},view(move));
  const folderUnknown='the App has not received this conversation’s working folder, so it cannot compare this location with it';
  assert.ok(noFolder.includes(`⟦Path: /invented/a.txt⟧ — ${folderUnknown}; moved to ⟦Path: /invented/b.txt⟧ — ${folderUnknown}`),noFolder);
  // A folder the App cannot read as a full path is not compared with, for a file or a command's folder alike.
  const relativeProject={project:{kind:'folder',folder:'invented/pump-skid'},conversationFolder:'/invented',permissionProfile:null};
  assert.ok(render(files,relativeProject,view(move)).includes(`⟦Path: /invented/a.txt⟧ — ${projectUnknown}`));
  assert.doesNotMatch(words(render(files,relativeProject,view(move))),/OUTSIDE/);
  assert.match(words(render(command({cwd:'/invented'}),relativeProject)),new RegExp(`Where the working folder is: ${projectUnknown}\\.`));
  assert.match(words(render(command({cwd:'/invented'}),{project:{kind:'none'},conversationFolder:'tmp/c1',permissionProfile:null})),new RegExp(`Where the working folder is: ${folderUnknown}\\.`));
  // A known folder keeps the card's existing marks.
  assert.match(render(files,project,view([{path:'/invented/pump-skid/a.txt',kind:{type:'add'},diff:'+x\n'}])),/⟦Path: \/invented\/pump-skid\/a\.txt⟧ — in your project folder, at ⟦Path: a\.txt⟧/);
});

// The maintained consequence cases the host's sheet is also checked against (tests/fixtures/request_answer_cases.json),
// each rendered through the card: every expected sentence appears among the card's own words, and the case's
// answer is one the card offers. Curly and straight apostrophes are read alike.
test('each maintained consequence case reads on the card as the fixture states it',()=>{
  const cases=JSON.parse(readFileSync(new URL('./fixtures/request_answer_cases.json',import.meta.url),'utf8'));
  assert.ok(cases.length>=7);
  const plain=s=>s.replace(/[’‘]/g,"'");
  const keyOf=d=>typeof d==='string'?d:Object.keys(d)[0];
  for(const c of cases){
    const r=request(c.method,{threadId:'thread',turnId:'turn',itemId:'item',...c.params});
    const view=c.changes?{home:g.home,generation:g,items:[{threadId:'thread',turnId:'turn',native:{id:'item',type:'fileChange',status:'inProgress',changes:c.changes}}],turns:[],turnRecords:[],revisions:[],descendants:[]}:null;
    const place={project:c.project,conversationFolder:'/invented/project',permissionProfile:c.profile};
    const shown=plain(words(render(r,place,view)));
    for(const sentence of c.expected) assert.ok(shown.includes(plain(sentence)),`${c.name}: missing «${sentence}»\n${shown}`);
    for(const sentence of c.excluded??[]) assert.ok(!shown.includes(plain(sentence)),`${c.name}: contradictory «${sentence}»\n${shown}`);
    assert.ok(decisionForms(r).some(f=>JSON.stringify(f.decision)===JSON.stringify(c.decision)||keyOf(f.decision)===c.decision),`${c.name}: the card offers the case's answer`);
  }
});

test('legacy file moves resolve the destination and mark outside or unknown on the card',()=>{
  const r=request('applyPatchApproval',{conversationId:'T',callId:'move',fileChanges:{'source.txt':{type:'update',move_path:'../outside.txt',unified_diff:'+invented'}}});
  const shown=render(r,project);
  assert.match(shown,/Path: \/invented\/pump-skid\/source\.txt/);
  assert.match(shown,/moved to .*Path: \/invented\/outside\.txt.*OUTSIDE your project folder/);
  const unknown=render(r,{...project,project:{kind:'unknown'}});
  assert.match(unknown,/moved to .*Path: \/invented\/outside\.txt.*could not compare/);
  assert.doesNotMatch(words(unknown),/OUTSIDE|in your project folder/);
});
