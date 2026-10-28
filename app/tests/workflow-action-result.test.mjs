import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import React from 'react';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {App,WorkflowRootPanel} = loadSrc('App');
const nodes = (container,tag) => container.querySelectorAll(node => node.localName === tag);
const labelled = (container,label) => container.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
function freeze(value) {
  if (value && typeof value === 'object') {Object.values(value).forEach(freeze);Object.freeze(value);}
  return value;
}
let packet;
function actualPacket() {
  if (packet) return packet;
  let output;
  if (process.env.CHIRALITY_WORKFLOW_ACTION_RESULT_DTO_LOG) output = readFileSync(process.env.CHIRALITY_WORKFLOW_ACTION_RESULT_DTO_LOG,'utf8');
  else {
    const producer = 'runtime_session::workflow_root_tests::action_result_tests::workflow_action_actual_create_result_precedes_explicit_draft_observation';
    const result = spawnSync('cargo',['test','--offline','--locked','--lib',producer,'--','--exact','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:12*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);output = result.stdout;
  }
  const summary = Array.from(output.matchAll(/^test result: (ok|FAILED)\. (\d+) passed; (\d+) failed;/gm)).at(-1);
  assert.ok(summary?.[1] === 'ok' && Number(summary[2]) > 0 && Number(summary[3]) === 0,'actual offline Rust producer completed successfully');
  assert.match(output,/test runtime_session::workflow_root_tests::action_result_tests::workflow_action_actual_create_result_precedes_explicit_draft_observation/);
  const marker = 'WORKFLOW_ACTION_RESULT_DTO:';
  const captured = output.split('\n').filter(line => line.includes(marker)).map(line => JSON.parse(line.slice(line.indexOf(marker)+marker.length)));
  assert.equal(captured.length,1);
  const value = captured[0];
  assert.equal(value.standing.producer,'actual with_choice/verify_library_context → Root.create_selected_draft; unchanged mutation Value');
  assert.equal(value.beforeHostStatus.workflowRoot.drafts.drafts.length,0);
  assert.equal(value.afterWriteHostStatus.workflowRoot.drafts.drafts.length,0);
  assert.equal(value.afterObservedHostStatus.workflowRoot.drafts.drafts.length,1);
  assert.deepEqual(value.nativeResult.base,value.source.closedBase);
  packet = freeze(value);return packet;
}
const panelIn = container => nodes(container,'h2').find(node => node.textContent === 'Workflow selection and native registration').parentNode;
const createButton = container => nodes(panelIn(container),'button').find(node => node.textContent === 'Create draft from inspected content');
const resultText = container => labelled(panelIn(container),'Workflow command result')?.textContent ?? '';
const limits = container => panelIn(container).querySelectorAll(node => node.getAttribute('aria-label') === 'Workflow observation limit').map(node => node.textContent);
const relation = container => JSON.parse(nodes(nodes(labelled(panelIn(container),'Workflow action response'),'details')[0],'pre')[0].textContent);

async function mountedApp(t,{failFirstRefresh = false,metadataError,nativeRefusal = false,viewGate} = {}) {
  const source = actualPacket(),before = JSON.stringify(source),calls = [],unexpected = [];
  let primary = false,observed = false,failed = false,gated = false,externalHost;
  const idle = installIdleNativeWaiting(async (command,args) => {
    calls.push([command,structuredClone(args)]);
    if (command === 'host_status') {
      if (primary && failFirstRefresh && !failed) {failed = true;throw Error('Controlled original view refresh unavailable');}
      if (primary && viewGate && !gated) {gated = true;viewGate.started.resolve();return viewGate.reply.promise;}
      return externalHost ?? (nativeRefusal ? source.afterWriteHostStatus : observed ? source.afterObservedHostStatus : primary ? source.afterWriteHostStatus : source.beforeHostStatus);
    }
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === source.command) {
      assert.deepEqual(args,source.args);
      if (nativeRefusal) throw source.existingTargetRefusal.nativeError;
      assert.equal(primary,false,'one original mutation, never an observation retry');primary = true;return source.nativeResult;
    }
    if (command === source.explicitObservation.command) {
      assert.deepEqual(args,source.explicitObservation.args,'the automatic read retains the exact original context');
      assert.equal(observed,false,'automatic metadata observation occurs once');
      if (metadataError) throw metadataError;
      observed = true;return source.explicitObservation.nativeResult;
    }
    unexpected.push(command);throw Error(`Unexpected business/read command: ${command}`);
  });
  t.mock.timers.enable({apis:['setInterval']});
  const container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
  await React.act(async () => {root.render(React.createElement(App));});
  const name = nodes(panelIn(container),'label').find(node => node.textContent.startsWith('New draft name'));
  await React.act(() => props(nodes(name,'input')[0]).onChange({target:{value:source.args.name}}));
  idle.assertClean(container);
  return {container,calls,source,setExternalHost:host => {externalHost = host;},close:async () => {
    idle.assertClean(container);const text = container.textContent;
    await React.act(async () => {root.unmount();});document.body.removeChild(container);idle.restore(text);
    assert.equal(idle.calls.filter(row => row.command === 'plugin:event|listen').length,1);
    assert.equal(idle.calls.filter(row => row.command === 'plugin:event|unlisten').length,1);
    assert.deepEqual(unexpected,[]);assert.equal(JSON.stringify(source),before,'the producer packet remains unchanged');
  }};
}

test('actual create result remains unchanged through a failed view refresh and one original draft observation',async t => {
  const view = await mountedApp(t,{failFirstRefresh:true});
  try {
    const start = view.calls.length;let returned;
    assert.equal(!!props(createButton(view.container)).disabled,false);
    await React.act(async () => {returned = await props(createButton(view.container)).onClick();});
    assert.equal(returned,view.source.nativeResult,'the leaf receives the unchanged native Value, not a UI envelope');
    assert.equal(resultText(view.container),JSON.stringify(view.source.nativeResult));
    assert.equal(limits(view.container).length,1);
    assert.ok(limits(view.container)[0].includes('View refresh after workflow_create_draft failed: Error: Controlled original view refresh unavailable'));
    assert.ok(limits(view.container)[0].includes('response is retained as reported'));
    assert.deepEqual(relation(view.container),{command:view.source.command,source:view.source.beforeHostStatus.workflowRoot.context,request:view.source.args});
    assert.deepEqual(view.calls.slice(start).map(([command]) => command),['workflow_create_draft','host_status','workflow_observe_drafts','host_status','decision_view']);
    assert.ok(labelled(panelIn(view.container),'Workflow drafts').textContent.includes('draft — not registered'),'the explicit observation is visible after the later view read');
    assert.equal(view.calls.filter(([command]) => command === 'workflow_create_draft').length,1);
    assert.equal(view.calls.filter(([command]) => command === 'workflow_observe_drafts').length,1);
  } finally {await view.close();}
});

test('actual create success retains its happy-path cadence and native existing-target refusal remains as given',async t => {
  for (const nativeRefusal of [false,true]) await t.test(nativeRefusal ? 'existing target refusal' : 'successful refresh',async st => {
    const view = await mountedApp(st,{nativeRefusal});
    try {
      const start = view.calls.length;let returned;
      await React.act(async () => {returned = await props(createButton(view.container)).onClick();});
      assert.deepEqual(limits(view.container),[]);
      if (nativeRefusal) {
        assert.equal(returned,undefined);assert.equal(resultText(view.container),view.source.existingTargetRefusal.nativeError);
        assert.deepEqual(view.calls.slice(start).map(([command]) => command),['workflow_create_draft']);
        // This particular producer refusal precedes copying. No claim about
        // generic command errors, which can follow partial I/O, is inferred.
      } else {
        assert.equal(returned,view.source.nativeResult);assert.equal(resultText(view.container),JSON.stringify(view.source.nativeResult));
        assert.deepEqual(view.calls.slice(start).map(([command]) => command),['workflow_create_draft','host_status','decision_view','workflow_observe_drafts','host_status','decision_view']);
      }
    } finally {await view.close();}
  });
});

test('a metadata observation refusal names its limit without replacing the actual primary result',async t => {
  // Derived metadata-read failure; the primary Value/context remain the
  // actual producer bytes. This error is no additional native witness.
  const view = await mountedApp(t,{metadataError:'Controlled metadata read refused'});
  try {
    const start = view.calls.length;let returned;
    await React.act(async () => {returned = await props(createButton(view.container)).onClick();});
    assert.equal(returned,view.source.nativeResult);assert.equal(resultText(view.container),JSON.stringify(view.source.nativeResult));
    assert.equal(limits(view.container).length,1);
    assert.ok(limits(view.container)[0].includes('Draft observation (workflow_observe_drafts) after workflow_create_draft failed: Controlled metadata read refused'));
    assert.deepEqual(view.calls.slice(start).map(([command]) => command),['workflow_create_draft','host_status','decision_view','workflow_observe_drafts']);
  } finally {await view.close();}
});

test('a delayed view failure after a source switch keeps the original receipt and metadata request without replacing the current choice',async t => {
  // Derived observer timing/source switch. Mutation result, original args
  // and follow-up args are still the unchanged actual producer fields.
  const gate = {started:Promise.withResolvers(),reply:Promise.withResolvers()};
  const view = await mountedApp(t,{viewGate:gate,metadataError:'Controlled original source is no longer current'});
  let pending,returned;
  try {
    await React.act(async () => {pending = props(createButton(view.container)).onClick();await gate.started.promise;});
    assert.equal(resultText(view.container),JSON.stringify(view.source.nativeResult),'the completed response is visible while the observer is pending');
    assert.equal(props(createButton(view.container)).disabled,true);
    const replacement = structuredClone(view.source.beforeHostStatus);
    replacement.workflowRoot.context.sourceRef = 'synthetic-replacement-workflow-source';
    replacement.workflowRoot.activeLibrary = 'synthetic-replacement-library';
    replacement.workflowRoot.inspection.reference = 'synthetic-replacement-inspection';
    replacement.workflowRoot.inspection.identity.name = 'synthetic-replacement-method';
    view.setExternalHost(replacement);
    await React.act(async () => {t.mock.timers.tick(1000);});
    assert.ok(panelIn(view.container).textContent.includes('Inspected: synthetic-replacement-method'));
    await React.act(async () => {gate.reply.reject(Error('Controlled original refresh failed after source switch'));returned = await pending;});
    assert.equal(returned,view.source.nativeResult);
    assert.equal(resultText(view.container),JSON.stringify(view.source.nativeResult));
    assert.deepEqual(relation(view.container),{command:view.source.command,source:view.source.beforeHostStatus.workflowRoot.context,request:view.source.args});
    assert.equal(limits(view.container).length,2);
    assert.ok(limits(view.container).some(value => value.includes('Controlled original source is no longer current')));
    assert.ok(panelIn(view.container).textContent.includes('Inspected: synthetic-replacement-method'),'an old response never becomes the current selection');
    assert.deepEqual(view.calls.filter(([command]) => command === 'workflow_observe_drafts'),[[view.source.explicitObservation.command,view.source.explicitObservation.args]]);
    assert.equal(view.calls.filter(([command]) => command === view.source.command).length,1);
  } finally {gate.reply.resolve(actualPacket().afterWriteHostStatus);if (pending) await React.act(async () => {await pending;});await view.close();}
});

async function mountedPanel({data,host,act,observeView}) {
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke:async command => {assert.fail(`Unexpected direct-panel IPC: ${command}`);}};
  const container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
  await React.act(() => root.render(React.createElement(WorkflowRootPanel,{data,host,act,observeView})));
  return {container,close:async () => {await React.act(() => root.unmount());document.body.removeChild(container);window.__TAURI_INTERNALS__ = previous;}};
}

test('Refine retains its raw result and observes the captured original library even when its reply names another library',async () => {
  // Derived legacy Refine callback control, not a Rust Refine result or act.
  // The original source/context comes from the actual no-chat producer basis.
  const source = actualPacket(),data = source.beforeHostStatus.workflowRoot,calls = [];
  const nativeValue = freeze({syntheticRefineResult:true,library:'synthetic-other-returned-library'});
  let observations = 0;
  const view = await mountedPanel({data,host:source.beforeHostStatus,observeView:async () => {observations++;throw Error('Controlled view refresh unavailable');},
    act:async (command,args) => {
      calls.push([command,structuredClone(args)]);
      if (command === 'workflow_refine_registered') return nativeValue;
      assert.equal(command,'workflow_observe_drafts');assert.deepEqual(args,source.explicitObservation.args);return source.explicitObservation.nativeResult;
    }});
  try {
    const nameLabel = nodes(view.container,'label').find(node => node.textContent.startsWith('New draft name'));
    const revisionLabel = nodes(view.container,'label').find(node => node.textContent.startsWith('Registered revision'));
    await React.act(() => {props(nodes(nameLabel,'input')[0]).onChange({target:{value:source.args.name}});props(nodes(revisionLabel,'input')[0]).onChange({target:{value:source.nativeResult.base.revision}});});
    const button = nodes(view.container,'button').find(node => node.textContent === 'Refine registered revision from the revision store (no selection)');
    let returned;await React.act(async () => {returned = await props(button).onClick();});
    assert.equal(returned,nativeValue);assert.equal(resultText(view.container),JSON.stringify(nativeValue));
    assert.deepEqual(calls,[['workflow_refine_registered',{name:source.args.name,revision:source.nativeResult.base.revision}],['workflow_observe_drafts',source.explicitObservation.args]]);
    assert.equal(observations,2);assert.equal(limits(view.container).length,2);
    assert.deepEqual(relation(view.container).request,{name:source.args.name,revision:source.nativeResult.base.revision},'the legacy mutation receives no invented context argument');
  } finally {await view.close();}
});

test('the real Compare child receives its raw result through RootPanel even when the later view observer fails',async () => {
  // Derived trial selection, with the repository's existing Rust-shaped
  // comparison fixture. This checks the shared child return-value contract.
  const source = actualPacket(),data = structuredClone(source.afterObservedHostStatus.workflowRoot);
  data.drafts.drafts[0].trials = ['trial:synthetic-one','trial:synthetic-two'].map((reference,index) => ({reference,sequence:index+1,kind:'delegated',version:'current',
    content:data.drafts.drafts[0].content,subAgent:{state:'sub-agent not linked'},fidelity:{state:'not checked',limits:[]},broughtBack:[],live:false}));
  const nativeValue = freeze(JSON.parse(readFileSync(new URL('./fixtures/trial-compare.json',import.meta.url),'utf8'))),calls = [];
  const view = await mountedPanel({data,host:{...source.afterObservedHostStatus,workflowRoot:data},observeView:async () => {throw Error('Controlled Compare view refresh failed');},
    act:async (command,args) => {calls.push([command,args]);assert.equal(command,'workflow_trial_compare');return nativeValue;}});
  try {
    const choices = nodes(view.container,'label').filter(node => node.textContent.trim() === 'Compare');
    assert.equal(choices.length,2);
    for (let index = 0;index < 2;index++) {
      const current = nodes(view.container,'label').filter(node => node.textContent.trim() === 'Compare')[index];
      await React.act(() => props(nodes(current,'input')[0]).onChange());
    }
    const button = nodes(view.container,'button').find(node => node.textContent === 'Compare');assert.equal(props(button).disabled,false);
    await React.act(async () => {props(button).onClick();await new Promise(resolve => setImmediate(resolve));});
    assert.deepEqual(calls,[['workflow_trial_compare',{left:{trial:'trial:synthetic-one'},right:{trial:'trial:synthetic-two'}}]]);
    assert.ok(labelled(view.container,'Compare result').textContent.includes(nativeValue.standing),'the child stores and renders the native comparison, not undefined or an envelope');
    assert.equal(resultText(view.container),JSON.stringify(nativeValue));assert.equal(limits(view.container).length,1);
  } finally {await view.close();}
});
