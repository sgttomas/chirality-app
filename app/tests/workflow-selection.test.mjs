import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
const document=installMiniDom();
const React=(await import('react')).default;
const {createRoot}=await import('react-dom/client');
const {WorkflowRootPanel}=loadSrc('App');
const {chatWorkflow,workflowContext,workflowArguments}=loadSrc('workflowSelection');
const g={appSession:'invented-session',home:'invented-home-a',spawnCounter:1};
const choice=(reference,name)=>({reference,identity:{name,origin:'project',revision:reference},standing:'registered revision',runnable:true});
const data={context:{sourceRef:'owned-home-a',generation:g,historyEpoch:7},activeLibrary:'library-a',libraries:[],reviews:[],
  inspection:{...choice('inspected','library content'),runnable:false},selections:[
    {sourceRef:'owned-home-a',threadId:'chat-1',selection:choice('selection-a','workflow A')},
    {sourceRef:'owned-home-a',threadId:'chat-2',selection:choice('selection-b','workflow B')},
    {sourceRef:'owned-home-b',threadId:'chat-1',selection:choice('foreign','foreign home choice')}],runs:[]};
const host={state:'ready',generation:g,workflowRoot:data,threads:['chat-1','chat-2','new-chat'].map(threadId=>({threadId,generation:g}))};
const props=el=>el[Object.keys(el).find(k=>k.startsWith('__reactProps$'))];
const all=(container,name)=>container.querySelectorAll(e=>e.localName===name);
const press=async(container,label)=>{const button=all(container,'button').find(e=>e.textContent===label);assert.ok(button,label);assert.equal(props(button).disabled,false);await React.act(async()=>{props(button).onClick();await new Promise(r=>setTimeout(r,0));});};

test('pending lookup is qualified by App source and chat, without inspection fallback',()=>{
  assert.equal(chatWorkflow(data,'owned-home-a','chat-1').identity.name,'workflow A');
  assert.equal(chatWorkflow(data,'owned-home-a','chat-2').identity.name,'workflow B');
  assert.equal(chatWorkflow(data,'owned-home-b','chat-1').identity.name,'foreign home choice');
  assert.equal(chatWorkflow(data,'owned-home-a','new-chat'),undefined);
  assert.equal(chatWorkflow(data,'owned-home-a',''),undefined);
});
test('each press freezes the displayed full source, chat, history and choice reference',()=>{
  const args=workflowArguments('workflow_select_listed',{libraryRef:'library-a',name:'workflow',revision:'r'},data,host,'chat-1');
  assert.deepEqual(args.context,{sourceRef:'owned-home-a',generation:g,historyEpoch:7,threadId:'chat-1',selectionRef:'selection-a',inspectionRef:'inspected',libraryRef:'library-a'});
  const mutable=structuredClone(data);const snapshot=workflowContext(mutable,{...host,workflowRoot:mutable},'chat-2');
  mutable.context.generation.spawnCounter=2;mutable.selections[1].selection.reference='changed';
  assert.equal(snapshot.generation.spawnCounter,1);assert.equal(snapshot.selectionRef,'selection-b');
  assert.equal(workflowContext(data,{...host,generation:{...g,spawnCounter:2}},'chat-1'),undefined);
  assert.equal(workflowContext(data,{...host,workflowRoot:{context:{sourceRef:'changed-source'}}},''),undefined);
  assert.equal(workflowContext(data,host,'unloaded'),undefined);
  assert.throws(()=>workflowArguments('workflow_prepare_run',{threadId:'unloaded'},data,host,'chat-1'),/source or chat changed/);
});
test('no-chat browsing remains available before Codex starts and never names a new chat',()=>{
  const cold={context:{sourceRef:'owned-cold-home',generation:null,historyEpoch:null},inspection:data.inspection,selections:[]};
  const h={generation:null,workflowRoot:cold,threads:[]};
  const context=workflowArguments('workflow_select_development',{},cold,h,'').context;
  assert.equal(context.threadId,null);assert.equal(context.selectionRef,null);assert.equal(context.inspectionRef,'inspected');
  assert.equal(workflowContext(cold,h,'new-chat'),undefined);
});
test('actual panel switches the visible chat choice and sends its exact context',async()=>{
  const calls=[];const act=async(c,a)=>{calls.push([c,a]);return {reference:'prepared'};};
  const container=document.createElement('div');document.body.appendChild(container);const root=createRoot(container);
  await React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data,host,act})));
  assert.match(container.textContent,/Inspection here selects no workflow for a new chat/);
  assert.match(container.textContent,/Inspected: library content/);
  const select=all(container,'select').find(e=>e.textContent.includes('No chat'));
  await React.act(()=>props(select).onChange({target:{value:'chat-1'}}));
  assert.match(container.textContent,/Selected: workflow A/);
  await press(container,'Prepare exact selected workflow text');
  assert.equal(calls[0][1].context.selectionRef,'selection-a');assert.equal(calls[0][1].threadId,'chat-1');
  await React.act(()=>props(select).onChange({target:{value:'chat-2'}}));
  assert.match(container.textContent,/Selected: workflow B/);
  await press(container,'Prepare exact selected workflow text');
  assert.equal(calls[1][1].context.selectionRef,'selection-b');assert.equal(calls[1][1].threadId,'chat-2');
  await React.act(()=>props(select).onChange({target:{value:'new-chat'}}));
  assert.match(container.textContent,/No workflow selected/);
  const prepare=all(container,'button').find(e=>e.textContent==='Prepare exact selected workflow text');assert.equal(props(prepare).disabled,true);
  assert.equal(calls.length,2,'switching or a new chat sends nothing');
  const switched={...host,generation:{...g,home:'invented-home-b'},workflowRoot:{...data,context:{...data.context,sourceRef:'owned-home-b',generation:{...g,home:'invented-home-b'}}}};
  await React.act(()=>root.render(React.createElement(WorkflowRootPanel,{data:switched.workflowRoot,host:switched,act})));
  assert.match(container.textContent,/Inspection here selects no workflow for a new chat/);
  assert.equal(calls.length,2,'home switch neither propagates nor sends a choice');
  await React.act(()=>root.unmount());
});
