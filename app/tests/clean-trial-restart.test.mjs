import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import React from 'react';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {WorkflowRootPanel,ConversationPanel} = loadSrc('App');
const {conversationKey,findConversation} = loadSrc('TrialComposer');
const {TrialRow,initialDraftsState} = loadSrc('WorkflowDrafts');
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
const nodes = (container,tag) => container.querySelectorAll(node => node.localName === tag);
const button = (container,label) => nodes(container,'button').find(node => node.textContent === label);
async function press(container,label) {
  const control = button(container,label);
  assert.ok(control,label);
  assert.equal(!!props(control).disabled,false,label);
  await React.act(async () => {await props(control).onClick();});
}
async function choose(control,value) {
  assert.ok(control);
  assert.equal(!!props(control).disabled,false);
  await React.act(() => props(control).onChange({target:{value}}));
}

let packet;
function actualRestartPacket() {
  if (packet) return packet;
  let output;
  if (process.env.CHIRALITY_CLEAN_TRIAL_RESTART_DTO_LOG) output = readFileSync(process.env.CHIRALITY_CLEAN_TRIAL_RESTART_DTO_LOG,'utf8');
  else {
    const result = spawnSync('cargo',['test','--offline','--locked','--lib','runtime_session::workflow_root_tests::trial_restart_source_tests','--','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:12*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);
    output = result.stdout;
  }
  const summary = Array.from(output.matchAll(/^test result: (ok|FAILED)\. (\d+) passed; (\d+) failed;/gm)).at(-1);
  assert.ok(summary?.[1] === 'ok' && Number(summary[2]) > 0 && Number(summary[3]) === 0,'actual Rust restart-source checks completed successfully');
  assert.match(output,/test runtime_session::workflow_root_tests::trial_restart_source_tests::/);
  const captured = marker => output.split('\n').filter(line => line.includes(marker)).map(line => JSON.parse(line.slice(line.indexOf(marker)+marker.length)));
  const main = captured('CLEAN_TRIAL_RESTART_DTO:');
  assert.equal(main.length,1,'one actual post-restart evidence packet');
  const unqualified = captured('CLEAN_TRIAL_RESTART_UNQUALIFIED_DTO:');
  assert.equal(unqualified.length,1,'one actual legacy/delegated source packet');
  packet = {...main[0],refusals:captured('CLEAN_TRIAL_RESTART_REFUSAL_DTO:'),unqualifiedRows:unqualified[0].unqualifiedRows,
    metadata:captured('CLEAN_TRIAL_RESTART_METADATA_DTO:')};
  return packet;
}

// Use the production panels, including their composer filtering and choice
// state. The transport supplies only captured Rust results and snapshots.
function mountPanels({workflowRoot,host,route}) {
  const calls = [];
  const previous = window.__TAURI_INTERNALS__;
  window.__TAURI_INTERNALS__ = {invoke:async (name,args) => {
    calls.push([name,structuredClone(args)]);
    throw Error(`Unexpected direct native invocation: ${name}`);
  }};
  function Panels() {
    const [data,setData] = React.useState(workflowRoot);
    const [threadKey,setThreadKey] = React.useState('');
    const act = async (name,args) => {
      calls.push([name,structuredClone(args)]);
      const response = await route(name,args);
      if (response.workflowRoot) setData(response.workflowRoot);
      if (Object.hasOwn(response,'error')) throw response.error;
      return response.result;
    };
    const unexpected = async () => {throw Error('Unexpected conversation action');};
    const current = {...host,workflowRoot:data};
    return React.createElement(React.Fragment,null,
      React.createElement(WorkflowRootPanel,{data,host:current,act}),
      React.createElement(ConversationPanel,{host:current,threadKey,setThreadKey,runAct:act,trialRunAct:act,codexBusy:false,
        answer:unexpected,send:unexpected,steer:unexpected,submitAttachments:unexpected,interrupt:unexpected,checkPlanMode:unexpected}));
  }
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  return {container,calls,show:async () => React.act(() => root.render(React.createElement(Panels))),
    close:async () => {await React.act(() => root.unmount());document.body.removeChild(container);window.__TAURI_INTERNALS__ = previous;}};
}

const labelled = (container,label) => container.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const trialModels = root => (root.drafts?.drafts ?? []).flatMap(draft => (draft.trials ?? []).map(trial => ({draft,trial})));
function trialElement(container,model) {
  const draft = labelled(container,`Draft ${model.draft.name}`);
  return labelled(draft,`Trial ${model.trial.sequence}`);
}

const hostFor = source => ({state:'ready',generation:source.target.generation,threads:source.conversations});
const modelFor = (root,reference) => {
  const model = trialModels(root).find(model => model.trial.reference === reference);
  assert.ok(model,`actual listed trial ${reference}`);
  return model;
};
async function showCurrentTarget(container,target) {
  const conversation = container.querySelectorAll(node => node.getAttribute('id') === 'conversation')[0];
  await choose(nodes(conversation,'select')[0],conversationKey(target));
}

test('actual cold clean source supports explicit reads and feedback while its authoring target stays unknown', async () => {
  const source = actualRestartPacket();
  const left = source.compare.left.trial,right = source.compare.right.trial;
  assert.ok(left && right && left !== right,'Compare receives two distinct actual trial sides');
  const original = modelFor(source.restored,left);
  assert.equal(original.trial.kind,'clean');
  assert.ok(original.trial.recordedNativeSource,'the host separately supplies the qualified recorded clean source');
  assert.ok(!original.trial.sourceLimit);
  assert.equal(original.trial.readAgain.offered,true);
  assert.ok(original.trial.authoringSourceLimit,'the restored source does not restore original authoring identity');
  assert.equal(findConversation(source.conversations,original.trial.authoringConversation),null);
  const afterRead = modelFor(source.afterRead,left);
  assert.equal(source.readResult.reference,left);
  assert.ok(source.readResult.source,'the actual read result retains its own source proof');
  assert.deepEqual(afterRead.trial.fidelity,source.readResult.recorded.at(-1).fidelity,'the row follows the actual read observation, not the source proof alone');
  assert.deepEqual(afterRead.trial.link,original.trial.link,'reading appends an observation without rebinding the saved trial');
  assert.deepEqual(source.afterRead.runs,source.restored.runs,'a history read opens no workflow run');
  const pending = source.bringBack.root.pendingBringBacks.find(row => row.trial === left);
  assert.ok(pending,'the actual bring-back command produced a separate unsent composer');
  assert.deepEqual(pending.target,source.target);
  assert.ok(pending.source?.standing,'the transcript keeps its own source qualification');
  const view = mountPanels({workflowRoot:source.restored,host:hostFor(source),route:async (name,args) => {
    if (name === 'workflow_trial_read') {
      assert.deepEqual(args,{reference:left});
      return {result:source.readResult,workflowRoot:source.afterRead};
    }
    if (name === 'workflow_trial_compare') {
      assert.deepEqual(args,{left:source.compare.left,right:source.compare.right});
      return {result:source.compare.result};
    }
    if (name === 'workflow_trial_bring_back') {
      assert.deepEqual(args,{reference:left,generation:source.target.generation,threadId:source.target.threadId,includeNative:false});
      return {result:source.bringBack.result,workflowRoot:source.bringBack.root};
    }
    if (name === 'workflow_bring_back_send') {
      assert.deepEqual(args,{id:pending.id,generation:source.target.generation,threadId:source.target.threadId,personText:source.send.personText});
      return {result:source.send.result,workflowRoot:source.send.root};
    }
    throw Error(`Unexpected action: ${name}`);
  }});
  try {
    await view.show();
    assert.deepEqual(view.calls,[],'mounting the recovered workspace performs no host calls');
    let row = trialElement(view.container,original);
    assert.ok(row.textContent.includes(original.trial.authoringSourceLimit));
    assert.equal(props(nodes(row,'select')[0]).value,'','no bare saved ID supplies an implicit target');
    assert.equal(!!props(button(row,'Bring trial back')).disabled,true);
    assert.equal(!!props(button(row,'Read again')).disabled,false,'read-source availability is independent of the authoring target');
    await showCurrentTarget(view.container,source.target);
    assert.deepEqual(view.calls,[],'choosing the current conversation does not read or prefill feedback');
    assert.equal(props(nodes(row,'select')[0]).value,'','the trial still requires its own explicit feedback target');
    await press(row,'Read again');
    assert.deepEqual(view.calls,[['workflow_trial_read',{reference:left}]]);
    assert.ok(view.container.textContent.includes(JSON.stringify(source.readResult)),'the existing read-result status retains source and observation evidence');
    row = trialElement(view.container,afterRead);
    if (afterRead.trial.fidelity.state === 'verbatim') assert.match(row.textContent,/workflow given verbatim/);
    else if (afterRead.trial.fidelity.state === 'differs') assert.match(row.textContent,/trial conversation's input differs from the run text/);
    else assert.match(row.textContent,/not checked/);
    assert.ok(row.textContent.includes(afterRead.trial.authoringSourceLimit));
    for (const reference of [left,right]) {
      const element = trialElement(view.container,modelFor(source.afterRead,reference));
      const compare = nodes(element,'input').find(node => props(node).type === 'checkbox');
      await React.act(() => props(compare).onChange({target:{checked:true}}));
    }
    await press(labelled(view.container,'Compare trials'),'Compare');
    assert.deepEqual(view.calls[1],['workflow_trial_compare',{left:source.compare.left,right:source.compare.right}]);
    const comparison = labelled(view.container,'Compare result');
    assert.ok(comparison);
    for (const side of [source.compare.result.left,source.compare.result.right]) {
      assert.ok(Number(side.summary.turns) > 0,'the actual Compare includes source history, not just empty version metadata');
      assert.ok(comparison.textContent.includes(side.label));
    }
    assert.match(comparison.textContent,/Version difference/);
    assert.ok(comparison.textContent.includes(source.compare.result.standing));
    await choose(nodes(row,'select')[0],conversationKey(source.target));
    assert.equal(view.calls.length,2,'choosing a target is not Bring back or Send');
    await press(row,'Bring trial back');
    assert.equal(view.calls[2][0],'workflow_trial_bring_back');
    const composer = labelled(view.container,'Bring back composer');
    assert.ok(composer,'the production conversation filter shows the pending transcript at the chosen target');
    assert.match(composer.textContent,/pre-filled, not sent/);
    assert.ok(composer.textContent.includes(pending.transcript));
    assert.ok(composer.textContent.includes(pending.source.standing));
    assert.equal(view.calls.length,3,'prefilling never submits a conversation turn');
    const prompt = nodes(composer,'textarea')[0];
    await React.act(() => props(prompt).onChange({target:{value:source.send.personText}}));
    assert.equal(view.calls.length,3,'editing the actual assessment text remains unsent');
    await press(composer,'Send');
    assert.deepEqual(view.calls[3],['workflow_bring_back_send',{id:pending.id,generation:source.target.generation,threadId:source.target.threadId,personText:source.send.personText}]);
    assert.ok(!(source.send.root.pendingBringBacks ?? []).some(row => row.id === pending.id),'the actual acknowledged send withdraws the original prefill');
    assert.equal(labelled(view.container,'Bring back composer'),undefined);
    assert.equal(view.calls.length,4,'no registration, selection, run start or additional send is introduced');
  } finally {await view.close();}
});

test('actual late source or link refusal stays named and creates no feedback prefill or implicit retarget', async () => {
  const source = actualRestartPacket();
  assert.ok(source.refusals.length >= 2,'actual source and link changes are both exercised');
  for (const refusal of source.refusals) {
    const model = modelFor(refusal.rootBefore,refusal.reference);
    const view = mountPanels({workflowRoot:refusal.rootBefore,host:hostFor(source),route:async (name,args) => {
      assert.equal(name,'workflow_trial_bring_back');
      assert.deepEqual(args,{reference:refusal.reference,generation:source.target.generation,threadId:source.target.threadId,includeNative:false});
      return {error:refusal.reason,workflowRoot:refusal.rootAfter};
    }});
    try {
      await view.show();
      assert.deepEqual(view.calls,[]);
      await showCurrentTarget(view.container,source.target);
      const row = trialElement(view.container,model);
      assert.equal(props(nodes(row,'select')[0]).value,'');
      await choose(nodes(row,'select')[0],conversationKey(source.target));
      assert.deepEqual(view.calls,[]);
      await press(row,'Bring trial back');
      assert.ok(view.container.textContent.includes(refusal.reason),'the actual source/link guard cause reaches the existing status');
      assert.equal((refusal.rootAfter.pendingBringBacks ?? []).length,0,'the actual guarded command leaves no prefill');
      assert.equal(labelled(view.container,'Bring back composer'),undefined);
      assert.deepEqual(view.calls,[['workflow_trial_bring_back',{reference:refusal.reference,generation:source.target.generation,threadId:source.target.threadId,includeNative:false}]],'the refusal does not try another source or target or send a message');
    } finally {await view.close();}
  }
});

test('actual legacy clean and delegated cold rows retain source limits after an explicit current target choice', async () => {
  const source = actualRestartPacket();
  assert.deepEqual([...new Set(source.unqualifiedRows.map(row => row.kind))].sort(),['clean','delegated']);
  for (const trial of source.unqualifiedRows) {
    assert.ok(trial.sourceLimit);
    assert.ok(trial.authoringSourceLimit);
    assert.equal(trial.readAgain.offered,false);
    assert.ok(!trial.recordedNativeSource,'a saved link alone is not the future clean source proof');
    const calls = [];
    function Row() {
      const [state,setState] = React.useState(initialDraftsState);
      return React.createElement(TrialRow,{trial,conversations:source.conversations,busy:false,state,update:patch => setState(old => ({...old,...patch})),act:async (...args) => {calls.push(args);}});
    }
    const container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
    try {
      await React.act(() => root.render(React.createElement(Row)));
      assert.deepEqual(calls,[]);
      assert.equal(props(nodes(container,'select')[0]).value,'');
      assert.ok(container.textContent.includes(trial.sourceLimit));
      assert.ok(container.textContent.includes(trial.authoringSourceLimit));
      assert.equal(button(container,'Read again'),undefined);
      await choose(nodes(container,'select')[0],conversationKey(source.target));
      assert.equal(!!props(button(container,'Bring trial back')).disabled,true,'explicit target choice cannot supply missing source evidence');
      assert.deepEqual(calls,[]);
    } finally {await React.act(() => root.unmount());document.body.removeChild(container);}
  }
});

test('actual source-recording phases distinguish a held save retry from an unavailable original observation', async () => {
  const source = actualRestartPacket();
  // The Rust producer exercises more than one failure at the held-save phase.
  // Require every phase, then exercise every captured row below.
  assert.deepEqual([...new Set(source.metadata.map(row => row.phase))].sort(),['saved-unavailable','unconfirmed-held','unheld']);
  for (const {phase,row:trial} of source.metadata) {
    const metadata = trial.sourceMetadata;
    assert.ok(metadata?.limit,'the actual recording failure keeps its cause');
    const calls = [];
    function Row({busy}) {
      const [state,setState] = React.useState(initialDraftsState);
      return React.createElement(TrialRow,{trial,conversations:source.conversations,busy,state,
        update:patch => setState(old => ({...old,...patch})),act:async (...args) => {calls.push(args);}});
    }
    const container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
    try {
      await React.act(() => root.render(React.createElement(Row,{busy:true})));
      const notice = labelled(container,'Restart history source recording');
      assert.ok(notice);
      assert.ok(notice.textContent.includes(metadata.persistence));
      assert.ok(notice.textContent.includes(metadata.limit));
      assert.match(notice.textContent,/trial's send outcome is unchanged/);
      for (const internal of [metadata.pointerIdentity,metadata.owner,metadata.value]) {
        if (typeof internal === 'string' && internal) assert.ok(!notice.textContent.includes(internal),'the source-recording notice does not print internal source tokens');
      }
      if (phase === 'unconfirmed-held') {
        assert.equal(metadata.heldMetadata,true);
        assert.match(notice.textContent,/source record: save not confirmed/);
      } else if (phase === 'saved-unavailable') {
        assert.equal(metadata.heldMetadata,true);
        assert.match(notice.textContent,/source record: saved; the App cannot currently recheck the saved record/);
      } else {
        assert.equal(metadata.heldMetadata,false);
        assert.match(notice.textContent,/original source observation is not held/);
      }
      if (metadata.heldMetadata) {
        assert.match(notice.textContent,/Read again also retries saving this original source record\. It never resends the trial/);
      } else {
        assert.match(notice.textContent,/No original source record is held for a save retry/);
        assert.doesNotMatch(notice.textContent,/Read again also retries saving/);
      }
      assert.deepEqual(calls,[],'rendering a recording limit neither retries metadata nor resends a trial');
      assert.equal(!!props(button(container,'Read again')).disabled,true,'source recording display preserves the existing busy boundary');
      assert.equal(!!props(button(container,'Bring trial back')).disabled,true);
      await React.act(() => root.render(React.createElement(Row,{busy:false})));
      assert.deepEqual(calls,[],'becoming idle performs no automatic retry');
      await press(container,'Read again');
      assert.deepEqual(calls,[['workflow_trial_read',{reference:trial.reference}]],'the existing explicit read sends only the original trial reference, with no new send or source override');
    } finally {await React.act(() => root.unmount());document.body.removeChild(container);}
  }
});
