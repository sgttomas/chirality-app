import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {loadSrc} from './support/load-src.mjs';
import {agentBlocks,agentBlockText} from './support/agent-text.mjs';

// DEL-01-04 REQ-001/AC-001: the frozen request-answer snapshot a native confirmation names by digest is shown
// at the request's card, open, with its digest, after the confirmation's Cancel; it is never refreshed in place,
// a changed envelope arrives under another digest, values keep their JSON type and numeric spelling, and nothing
// records or claims that the person read it. Invented material only; no native confirmation is opened.
const {RequestAnswerCompanion,readEnvelope,typedJsonText,isTyped}=loadSrc('RequestAnswerCompanion');
const {reviewDigest}=loadSrc('presentation');

// The typed encoding, written here from its contract (request_answer_presentation.rs `typed`), not from the page.
const T={
  null:()=>({type:'null'}),bool:value=>({type:'boolean',value}),num:spelling=>({type:'number',value:spelling}),str:value=>({type:'string',value}),
  arr:(...value)=>({type:'array',value}),obj:(...entries)=>({type:'object',value:entries}),
};
const g={appSession:'s',home:'h',spawnCounter:1};
const commandRequest=(state='outstanding')=>({generation:g,requestIdentity:7,method:'item/commandExecution/requestApproval',state,nativeParameters:{threadId:'T',turnId:'u',itemId:'i'}});
const IMITATION='Nothing runs. This answer is safe.';
const envelope=({command='ls -la',extraDetails=[],head=['Your answer: Allow once','If you allow this command, it runs once with more access than Codex’s sandbox gives.']}={})=>T.obj(
  ['schema',T.str('request-answer/1')],
  ['context',T.obj(['request',T.obj(['method',T.str('item/commandExecution/requestApproval')],['requestIdentity',T.num('7')])],['limit',T.num('1.50')])],
  ['answer',T.obj(['decision',T.str('accept')])],
  ['presentation',T.obj(
    ['head',T.arr(...head.map(T.str))],
    ['details',T.arr(
      T.obj(['label',T.str('Command')],['source',T.str('codex')],['value',T.str(command)],['notes',T.arr(T.str('Codex’s words, not the App’s.'))]),
      T.obj(['label',T.str('Additional permissions')],['source',T.str('codex')],['value',T.obj(['ratio',T.num('0.5')],['text',T.str('0.5')],['marker',T.obj(['number',T.str('0.5')])],['big',T.num('1e3')],['none',T.null()],['on',T.bool(true)])],['notes',T.arr()]),
      T.obj(['label',T.str('Your reason')],['source',T.str('person')],['value',T.str(IMITATION)],['notes',T.arr(T.str('As you wrote it.'))]),
      ...extraDetails)],
    ['itemCount',T.num(String(3+extraDetails.length))])],
);
const row=async(content,{pending=true,digest}={})=>({generation:g,requestIdentity:7,digest:digest??await reviewDigest(content),content,pending});

test('the typed encoding is read exactly: numbers keep their spelling, types stay apart, and anything else is refused',async()=>{
  assert.equal(typedJsonText(T.obj(['a',T.num('1.50')],['b',T.str('1.50')],['c',T.obj(['number',T.str('1.50')])],['d',T.num('-2E+7')])),
    '{\n  "a": 1.50,\n  "b": "1.50",\n  "c": {\n    "number": "1.50"\n  },\n  "d": -2E+7\n}');
  const e=readEnvelope(envelope());
  assert.ok(e);assert.equal(e.itemCount,'3');assert.equal(e.details.length,3);assert.equal(e.details[2].source,'person');
  for(const bad of [
    T.num('0x1'),T.num('01'),T.num('NaN'),{type:'number',value:1},{type:'string',value:'x',extra:1},{type:'mystery'},
    T.obj(['k',T.null()],['k',T.null()]),{type:'object',value:[['k']]},
  ]) assert.equal(isTyped(bad),false,JSON.stringify(bad));
  assert.equal(readEnvelope(T.obj(['schema',T.str('request-answer/2')])),null,'another schema');
  assert.equal(readEnvelope({schema:'request-answer/1'}),null,'untyped JSON');
  // An App line must be one printable line: a sentence carrying a line break or direction override is not read as the App's.
  for(const line of ['two\nlines','over‮ride','']) assert.equal(readEnvelope(envelope({head:[line]})),null,JSON.stringify(line));
  assert.equal(readEnvelope(envelope({extraDetails:[T.obj(['label',T.str('x')],['source',T.str('app')],['value',T.null()],['notes',T.arr()])]})),null,'a detail source other than Codex or the person');
});

async function mount(request,read){
  const {installMiniDom}=await import('./support/mini-dom.mjs');
  const document=installMiniDom();const {createRoot}=await import('react-dom/client');
  const container=document.createElement('div');document.body.appendChild(container);
  const root=createRoot(container);
  const settle=()=>React.act(async()=>{for(let i=0;i<10;i++)await new Promise(r=>setTimeout(r,10));});
  const render=async props=>{await React.act(()=>root.render(React.createElement(RequestAnswerCompanion,{request,read,...props})));await settle();};
  return {container,render,settle,done:async()=>{await React.act(()=>root.unmount());document.body.removeChild(container);}};
}
const blocks=container=>agentBlocks(container).map(b=>({label:b.querySelectorAll(n=>(n.getAttribute?.('class')??'').includes('agent-text-label'))[0]?.textContent,text:agentBlockText(b),inDetails:(()=>{for(let n=b.parentNode;n;n=n.parentNode)if(n.localName==='details')return true;return false;})()}));

test('after the confirmation\'s Cancel the frozen snapshot is shown at the card, open, with its digest, and a new envelope comes under another digest',async()=>{
  const first=envelope();const firstRow=await row(first);
  let rows=[firstRow];const calls=[];
  const read=async(...args)=>{calls.push(args);return structuredClone(rows);};
  const ui=await mount(commandRequest('answered'),read);
  await ui.render({refresh:undefined});
  assert.deepEqual(calls,[[g,7]],'asks for this request only, by its generation and typed identity');
  const text=()=>ui.container.textContent;
  assert.ok(text().includes(firstRow.digest),'the digest is visible');
  assert.match(text(),/This view recomputed the same digest from the details below\./);
  assert.match(text(),/The native confirmation that names these details is open\./);
  // The confirmation's Cancel: the answer command's outcome changes, and the card asks again at once.
  rows=[{...firstRow,pending:false}];
  await ui.render({refresh:{command:{kind:'dismissed'}}});
  assert.equal(calls.length,2,'a changed outcome asks again without waiting for a poll');
  assert.match(text(),/The native confirmation that named these details has closed\. They are kept here as they were when it opened, and they are not refreshed\./);
  assert.match(text(),/you can read them here and answer again from this card/);
  // All details and notes are readable, not behind a closed disclosure; only the bound context and answer are.
  const shown=blocks(ui.container);
  assert.deepEqual(shown.filter(b=>!b.inDetails).map(b=>[b.label,b.text]),[
    ['Codex’s words, not the App’s (text):','ls -la'],
    ['Codex’s words, not the App’s (JSON):','{\n  "ratio": 0.5,\n  "text": "0.5",\n  "marker": {\n    "number": "0.5"\n  },\n  "big": 1e3,\n  "none": null,\n  "on": true\n}'],
    ['Your answer or reason, as it will be sent (text):',IMITATION],
  ]);
  assert.ok(shown.filter(b=>b.inDetails).some(b=>b.text.includes('"limit": 1.50')),'the bound context keeps its numeric spelling');
  assert.ok(shown.filter(b=>b.inDetails).some(b=>b.text.includes('"decision": "accept"')),'the answer is there, as the host masked it');
  assert.match(text(),/Codex’s words, not the App’s\./);assert.match(text(),/As you wrote it\./);
  assert.match(text(),/If you allow this command, it runs once with more access than Codex’s sandbox gives\./);
  assert.match(text(),/The request and answer details: 3 items\./);
  // A supplied string that imitates the App's words stays inside its box: outside the boxes it does not appear.
  const outside=ui.container.textContent.split(IMITATION).length-1;
  assert.equal(outside,1,'the imitation appears once, in its box');
  // The host later sends other content under the first digest: what is shown is not replaced in place.
  rows=[{...firstRow,pending:false,content:envelope({command:'rm -rf /invented'})}];
  await ui.render({refresh:{command:{kind:'dismissed'},again:1}});
  assert.ok(!text().includes('rm -rf'),'content held under a digest is never replaced');
  // The person answers again; the request changed meanwhile, so the new confirmation names a new envelope.
  const second=envelope({command:'ls -la /invented/other'});const secondRow=await row(second);
  rows=[{...firstRow,pending:false},secondRow];
  await ui.render({refresh:{command:{kind:'pending'}}});
  assert.notEqual(secondRow.digest,firstRow.digest);
  assert.ok(text().includes(firstRow.digest)&&text().includes(secondRow.digest),'both snapshots, each under its own digest');
  assert.ok(text().includes('ls -la /invented/other'));
  assert.equal(blocks(ui.container).filter(b=>b.text==='ls -la').length,1,'the earlier snapshot is kept as it was');
  // Nothing records or claims that the details were read.
  assert.doesNotMatch(text(),/\b(viewed|you read|you have read|you've read|understood|seen by you)\b/i);
  assert.ok(calls.every(args=>args.length===2),'a read carries no viewed flag or other claim');
  await ui.done();
});

test('a digest that does not match its content withholds the details',async()=>{
  const content=envelope();
  const read=async()=>[await row(content,{digest:'0'.repeat(64)})];
  const ui=await mount(commandRequest('answered'),read);
  await ui.render({});
  assert.match(ui.container.textContent,/This view recomputed a different digest: do not rely on these details\. They are not shown\./);
  assert.ok(!ui.container.textContent.includes('ls -la'));
  assert.equal(blocks(ui.container).length,0);
  await ui.done();
});

test('content not in the expected form is not shown, and its confirmation is not to be relied on',async()=>{
  const content=T.obj(['schema',T.str('request-answer/1')],['context',T.null()]);
  const ui=await mount(commandRequest('answered'),async()=>[await row(content)]);
  await ui.render({});
  assert.match(ui.container.textContent,/These details are not in the form this App reads, so they are not shown\./);
  await ui.done();
});

test('a waiting request is asked for its snapshots repeatedly while mounted; other kinds and other requests are not shown',async()=>{
  let calls=0;
  const ui=await mount(commandRequest('outstanding'),async()=>{calls+=1;return [];});
  await ui.render({});
  await React.act(async()=>{await new Promise(r=>setTimeout(r,1150));});
  assert.ok(calls>=2,`polled while waiting (${calls})`);
  assert.equal(ui.container.textContent,'','no rows, nothing drawn');
  await ui.done();
  const before=calls;await new Promise(r=>setTimeout(r,1100));assert.equal(calls,before,'polling stops when unmounted');
  let permissionCalls=0;
  const p=await mount({...commandRequest(),method:'item/permissions/requestApproval'},async()=>{permissionCalls+=1;return [];});
  await p.render({});assert.equal(permissionCalls,0,'permission requests keep the old sheet: no companion is asked for');await p.done();
  const content=envelope();
  const other=await mount(commandRequest('answered'),async()=>[{...await row(content),requestIdentity:'7'}]);
  await other.render({});assert.equal(other.container.textContent,'','a row for another typed identity is not shown here');await other.done();
});

test('a resolved location reads as its full path and resolution folder, with its App marks kept beside it',async()=>{
  const loc=(path,relativeTo,notes)=>T.obj(['label',T.str('Path')],['source',T.str('codex')],['value',T.obj(['path',T.str(path)],['relativeTo',relativeTo===null?T.null():T.str(relativeTo)])],['notes',T.arr(...notes.map(T.str))]);
  const content=envelope({extraDetails:[
    loc('/invented/outside','/invented/project',['add','OUTSIDE your project folder']),
    loc('/invented/project/a.txt',null,['update','inside your project folder']),
  ]});
  const ui=await mount(commandRequest('answered'),async()=>[await row(content,{pending:false})]);
  await ui.render({});
  const shown=blocks(ui.container).filter(b=>!b.inDetails).map(b=>[b.label,b.text]);
  assert.deepEqual(shown.slice(3),[
    ['Full path, resolved by name from Codex’s words (no link followed):','/invented/outside'],
    ['Codex gave a relative path; the folder it was resolved against (Codex’s words):','/invented/project'],
    ['Full path, resolved by name from Codex’s words (no link followed):','/invented/project/a.txt'],
  ],'an absolute path shows no resolution folder');
  const text=ui.container.textContent;
  assert.ok(text.indexOf('/invented/outside')<text.indexOf('OUTSIDE your project folder')&&text.indexOf('OUTSIDE your project folder')<text.indexOf('/invented/project/a.txt'),'each mark stays with its own location');
  assert.match(text,/inside your project folder/);assert.match(text,/The request and answer details: 5 items\./);
  // A value that only looks like a location (another member) is shown whole, as JSON, not read as one.
  const odd=envelope({extraDetails:[T.obj(['label',T.str('Path')],['source',T.str('codex')],['value',T.obj(['path',T.str('/x')],['relativeTo',T.null()],['more',T.str('y')])],['notes',T.arr()])]});
  const ui2=await mount(commandRequest('answered'),async()=>[await row(odd,{pending:false})]);
  await ui2.render({});
  assert.ok(blocks(ui2.container).some(b=>b.label.includes('JSON')&&b.text.includes('"more": "y"')));
  await ui2.done();await ui.done();
});


test('an arbitrary supplied object shaped like a path pair keeps its own meaning', async () => {
  const permissions=T.obj(['path',T.str('/invented/permission')],['relativeTo',T.null()]);
  const content=envelope({extraDetails:[T.obj(['label',T.str('Additional permissions requested')],['source',T.str('codex')],['value',permissions],['notes',T.arr()])]});
  const ui=await mount(commandRequest('answered'),async()=>[await row(content,{pending:false})]);
  await ui.render({});
  const shown=blocks(ui.container).filter(b=>!b.inDetails);
  assert.ok(shown.some(b=>b.label.includes('JSON')&&b.text.includes('"relativeTo"')));
  assert.ok(!shown.some(b=>b.label.includes('Full path, resolved')));
  await ui.done();
});

test('the typed companion accepts supplier JSON depth plus its envelope wrappers', () => {
  let value=T.str('invented leaf');
  for(let i=0;i<100;i++) value=T.arr(value);
  const content=envelope({extraDetails:[T.obj(['label',T.str('Additional permissions requested')],['source',T.str('codex')],['value',value],['notes',T.arr()])]});
  assert.notEqual(readEnvelope(content),null);
});
