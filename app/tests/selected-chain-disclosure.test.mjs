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
const {WorkflowRootPanel} = loadSrc('App');
const nodes = (container,tag) => container.querySelectorAll(node => node.localName === tag);
const labelled = (container,label) => container.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
const selectionFor = (host,thread) => host.workflowRoot.selections.find(row => row.sourceRef === host.workflowRoot.context.sourceRef && row.threadId === thread)?.selection;
const articleFor = (container,run) => nodes(container,'article').find(node => nodes(node,'h3').some(heading => heading.textContent === run));
const chainButton = article => nodes(article,'button').find(node => node.textContent.startsWith('End this run and start '));
function freeze(value) {
  if (value && typeof value === 'object') {Object.values(value).forEach(freeze);Object.freeze(value);}
  return value;
}
let packet;
function actualPacket() {
  if (packet) return packet;
  let output;
  if (process.env.CHIRALITY_SELECTED_CHAIN_DISCLOSURE_DTO_LOG) output = readFileSync(process.env.CHIRALITY_SELECTED_CHAIN_DISCLOSURE_DTO_LOG,'utf8');
  else {
    const producer = 'runtime_session::workflow_root_tests::selected_chain_disclosure_tests::selected_chain_actual_status_reports_b_before_the_ordinary_choice';
    const result = spawnSync('cargo',['test','--offline','--locked','--lib',producer,'--','--exact','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:12*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);output = result.stdout;
  }
  const summary = Array.from(output.matchAll(/^test result: (ok|FAILED)\. (\d+) passed; (\d+) failed;/gm)).at(-1);
  assert.ok(summary?.[1] === 'ok' && Number(summary[2]) > 0 && Number(summary[3]) === 0,'actual offline Rust producer completed successfully');
  assert.match(output,/test runtime_session::workflow_root_tests::selected_chain_disclosure_tests::selected_chain_actual_status_reports_b_before_the_ordinary_choice/);
  const marker = 'SELECTED_CHAIN_DISCLOSURE_DTO:';
  const captured = output.split('\n').filter(line => line.includes(marker)).map(line => JSON.parse(line.slice(line.indexOf(marker)+marker.length)));
  assert.equal(captured.length,1);
  assert.equal(captured[0].standing,'actual project_status_history → workflow_status_after_history → publish_context; read-only selected B beside open A');
  packet = freeze(captured[0]);
  return packet;
}
async function mount(sample,act = async () => ({state:'synthetic ordinary command result'})) {
  let shown = sample.hostStatus;
  const calls = [],reads = [],previous = window.__TAURI_INTERNALS__,reviewRefs = new Set();
  const container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
  window.__TAURI_INTERNALS__ = {invoke:async (command,args) => {
    assert.equal(command,'workflow_review_digest','the panel may only make its existing read-only review-digest IPC');
    assert.ok(reviewRefs.has(args.reviewRef));reads.push([command,args]);
    return {unavailable:'Synthetic digest reader outside a native confirmation'};
  }};
  const render = async (host = shown,data = host.workflowRoot) => {
    shown = host;
    for (const review of data.reviews ?? []) reviewRefs.add(review.reference);
    await React.act(() => root.render(React.createElement(WorkflowRootPanel,{data,host,
      act:async (command,args) => {calls.push([command,structuredClone(args)]);return act(command,args);}})));
  };
  await render();
  return {container,calls,reads,render,close:async () => {await React.act(() => root.unmount());document.body.removeChild(container);window.__TAURI_INTERNALS__ = previous;}};
}
const expectedChain = (sample,personText = '') => {
  const host = sample.hostStatus,data = host.workflowRoot;
  return ['workflow_end_and_start',{runRef:sample.currentRun,generation:host.generation,threadId:sample.threadId,personText,
    context:{sourceRef:data.context.sourceRef,generation:data.context.generation,historyEpoch:data.context.historyEpoch ?? null,
      threadId:sample.threadId,selectionRef:selectionFor(host,sample.threadId)?.reference ?? null,inspectionRef:data.inspection?.reference ?? null,libraryRef:data.activeLibrary ?? null}}];
};
async function enterPersonText(view,value) {
  const label = nodes(view.container,'label').find(node => node.textContent.startsWith('Person text'));
  const textarea = nodes(label,'textarea')[0];
  await React.act(() => props(textarea).onChange({target:{value}}));
}

test('actual selected B production packet reaches the owning run before the single ordinary chain choice',async t => {
  const source = actualPacket();
  for (const sample of source.cases) await t.test(sample.case,async st => {
    const {hostStatus:host,currentRun,threadId} = sample,data = host.workflowRoot;
    const run = data.runs.find(row => row.reference === currentRun),selected = selectionFor(host,threadId),report = selected.compatibility,p = report.preparation;
    assert.equal(run.conversation,threadId);assert.notEqual(run.workflow.revision,selected.identity.revision);
    assert.deepEqual(p.workflow,selected.identity);assert.equal(p.basis.conversation,threadId);
    const before = JSON.stringify(host),view = await mount(sample);
    try {
      const article = articleFor(view.container,currentRun),button = chainButton(article),disclosure = labelled(article,'Selected workflow for the next run');
      assert.ok(button);assert.equal(!!props(button).disabled,false,'unknown/unsupported remains an ordinary choice');
      assert.deepEqual(view.calls,[],'mount neither selects, ends, starts, prepares nor sends');
      st.diagnostic(JSON.stringify({case:sample.case,check:p.check.result,beforeChoiceDisclosure:!!disclosure,chainEnabled:!props(button).disabled,commandsDuringMount:view.calls.length}));
      assert.ok(disclosure,'selected B requires its own readable disclosure before the chain choice; A’s report is not B’s');
      assert.ok(article.childNodes.indexOf(disclosure) < article.childNodes.indexOf(button));
      for (const value of [threadId,selected.identity.kind,selected.identity.name,selected.identity.origin,selected.identity.source_root,selected.identity.revision,selected.identity.revision_method,report.holdingLibrary]) assert.ok(disclosure.textContent.includes(value),value);
      assert.ok(!disclosure.textContent.includes(run.workflow.revision),'same-named A is not substituted for B');
      for (const value of ['CK-1 selected candidate',report.statement,report.inventoryOrigin.source,report.r14,'Publication: not published','catalog edition not supplied','environment observation not supplied']) assert.ok(disclosure.textContent.includes(value),value);
      for (const row of p.requirements) for (const value of [row.name,row.purpose,row.reason]) assert.ok(disclosure.textContent.includes(value),value);
      for (const value of Object.values(p.basis).filter(value => typeof value === 'string')) assert.ok(disclosure.textContent.includes(value),value);
      assert.ok(disclosure.textContent.includes(JSON.stringify(p.basis.generation)));
      for (const limit of report.publication.factsNotSupplied) assert.ok(disclosure.textContent.includes(limit),limit);
      if (p.role.standing === 'unknown') {
        assert.ok(disclosure.textContent.includes(`not established (${p.role.reason})`));assert.ok(!disclosure.textContent.includes('this conversation has'));
      } else {
        assert.ok(disclosure.textContent.includes('this conversation has WORKING_ITEMS'));
        assert.ok(disclosure.textContent.includes('The workflow is written for HELP_HUMAN'));
        assert.ok(disclosure.textContent.includes('You may still start or continue the run.'));
      }
      const aPanel = labelled(article,'Run panel');
      assert.ok(!aPanel.contains(disclosure));assert.ok(!aPanel.textContent.includes('CK-1 selected candidate'));
      for (const entry of run.compatibility) assert.ok(aPanel.textContent.includes(entry.statement),'A retains its own report');
      const personText = 'Exact next input\nwith "quotes", Ω and trailing space ';
      await enterPersonText(view,personText);
      await React.act(async () => {await props(chainButton(articleFor(view.container,currentRun))).onClick();});
      assert.deepEqual(view.calls,[expectedChain(sample,personText)]);
      assert.ok(view.reads.every(([command]) => command === 'workflow_review_digest'));
      assert.equal(JSON.stringify(host),before,'the original packet is unchanged');
    } finally {await view.close();}
  });
});

test('a foreign-Home run with the same thread gets no borrowed successor; an older run generation in the owning Home still shows B',async () => {
  // Derived UI association controls, not additional native producer evidence.
  const sample = structuredClone(actualPacket().cases[0]),host = sample.hostStatus;
  const owner = host.workflowRoot.runs.find(run => run.reference === sample.currentRun);
  const foreign = {...structuredClone(owner),reference:'run:synthetic-foreign-A',home:'synthetic-foreign-home',generation:{...owner.generation,home:'synthetic-foreign-home'}};
  owner.generation = {...owner.generation,appSession:'synthetic-earlier-session',spawnCounter:0};
  host.workflowRoot.runs.unshift(foreign);
  const view = await mount(freeze(sample));
  try {
    const foreignArticle = articleFor(view.container,foreign.reference),ownArticle = articleFor(view.container,sample.currentRun);
    assert.equal(foreign.conversation,owner.conversation,'the negative case deliberately repeats the bare thread');
    assert.equal(!!props(chainButton(foreignArticle)).disabled,true,'the original button already refuses the inactive Home');
    assert.ok(!labelled(foreignArticle,'Selected workflow for the next run'),'current-Home B must not be presented as foreign A’s successor');
    const ownDisclosure = labelled(ownArticle,'Selected workflow for the next run');assert.ok(ownDisclosure);
    assert.ok(ownDisclosure.textContent.includes(selectionFor(host,sample.threadId).identity.revision));
    assert.equal(!!props(chainButton(ownArticle)).disabled,false,'the owning Home remains eligible despite an earlier run generation');
    assert.deepEqual(view.calls,[]);
    const endForeign = nodes(foreignArticle,'button').find(node => node.textContent === 'End run');
    assert.equal(props(endForeign).disabled,false,'plain End keeps its original availability');
  } finally {await view.close();}
});

test('duplicate names and bare threads in other sources do not replace B, another chosen chat does not retarget chaining, and inspection supplies no fallback',async () => {
  // Derived source/selection controls. Only the first test claims production
  // packet correspondence; these variants exercise the existing UI contract.
  const sample = structuredClone(actualPacket().cases[0]),host = sample.hostStatus,data = host.workflowRoot,selected = selectionFor(host,sample.threadId);
  const foreign = {sourceRef:'synthetic-foreign-source',threadId:sample.threadId,selection:structuredClone(selected)};
  foreign.selection.reference = 'synthetic-foreign-selection';foreign.selection.identity.source_root = 'Synthetic foreign source root';
  foreign.selection.identity.revision = 'synthetic-foreign-full-revision';foreign.selection.compatibility.statement = 'Synthetic foreign report must stay elsewhere';
  const otherChat = structuredClone(foreign);otherChat.sourceRef = data.context.sourceRef;otherChat.threadId = 'synthetic-other-chat';
  otherChat.selection.reference = 'synthetic-other-chat-selection';otherChat.selection.identity.source_root = 'Synthetic other-chat source root';
  data.selections.unshift(foreign,otherChat);
  data.inspection = {...structuredClone(foreign.selection),reference:'synthetic-inspection-only',runnable:true};
  host.threads.push({threadId:otherChat.threadId,generation:host.generation});
  const view = await mount(sample);
  try {
    const selector = nodes(view.container,'select').find(node => node.textContent.includes('No chat'));
    await React.act(() => props(selector).onChange({target:{value:otherChat.threadId}}));
    const article = articleFor(view.container,sample.currentRun),disclosure = labelled(article,'Selected workflow for the next run');assert.ok(disclosure);
    assert.ok(disclosure.textContent.includes(selected.identity.source_root));assert.ok(disclosure.textContent.includes(selected.identity.revision));
    for (const value of [foreign.selection.identity.source_root,otherChat.selection.identity.source_root,foreign.selection.compatibility.statement]) assert.ok(!disclosure.textContent.includes(value));
    assert.deepEqual(view.calls,[]);
    const personText = 'Explicit original run input';await enterPersonText(view,personText);
    await React.act(async () => {await props(chainButton(articleFor(view.container,sample.currentRun))).onClick();});
    assert.deepEqual(view.calls,[expectedChain(sample,personText)],'the run conversation supplies the context even when another chat is chosen in the panel');
    const end = nodes(articleFor(view.container,sample.currentRun),'button').find(node => node.textContent === 'End run');
    await React.act(async () => {await props(end).onClick();});
    assert.deepEqual(view.calls[1],['workflow_end_run',{runRef:sample.currentRun,finishedReport:null}]);
    await React.act(() => props(nodes(view.container,'select').find(node => node.textContent.includes('No chat'))).onChange({target:{value:''}}));
    const noOwnedChoice = structuredClone(host);
    noOwnedChoice.workflowRoot.selections = noOwnedChoice.workflowRoot.selections.filter(row => !(row.sourceRef === data.context.sourceRef && row.threadId === sample.threadId));
    await view.render(noOwnedChoice);
    const unselected = articleFor(view.container,sample.currentRun);
    assert.ok(!labelled(unselected,'Selected workflow for the next run'),'foreign same-thread choice, another chat and inspection are not B defaults');
    assert.equal(props(chainButton(unselected)).disabled,true);
    assert.equal(props(nodes(unselected,'button').find(node => node.textContent === 'End run')).disabled,false);
    assert.equal(view.calls.length,2,'changing selections performs no additional action');
  } finally {await view.close();}
});

test('unavailable evaluation and an explicit no-role reading remain advisory and distinct from an unknown original role',async () => {
  for (const mode of ['unavailable','not supplied','explicit no role']) {
    const sample = structuredClone(actualPacket().cases[0]),selected = selectionFor(sample.hostStatus,sample.threadId),original = selected.compatibility;
    if (mode === 'unavailable') selected.compatibility = {occasionLabel:'CK-1 selected candidate',preparation:null,limit:'Synthetic evaluation unavailable',holdingLibrary:original.holdingLibrary,advisory:true};
    else if (mode === 'not supplied') delete selected.compatibility;
    else {
      selected.compatibility.preparation.role = {standing:'app-observed',role:null,supply_ref:'synthetic-deliberate-no-role'};
      selected.compatibility.statement = 'Synthetic explicit no-role check does not pass';
    }
    freeze(sample);
    const before = JSON.stringify(sample.hostStatus),view = await mount(sample);
    try {
      const article = articleFor(view.container,sample.currentRun),disclosure = labelled(article,'Selected workflow for the next run');assert.ok(disclosure);
      assert.ok(disclosure.textContent.includes('never decides whether the run starts'));
      if (mode === 'explicit no role') {
        assert.ok(disclosure.textContent.includes('Role in force: no role'));
        assert.ok(!disclosure.textContent.includes('Role in force: not established'));
        assert.ok(disclosure.textContent.includes('this conversation has no role'));
      } else {
        assert.ok(disclosure.textContent.includes('no evaluation'));
        if (mode === 'unavailable') assert.ok(disclosure.textContent.includes('Synthetic evaluation unavailable'));
        else assert.ok(disclosure.textContent.includes('Holding library: not supplied'));
      }
      const button = chainButton(article);assert.equal(!!props(button).disabled,false);
      assert.deepEqual(view.calls,[]);
      await React.act(async () => {await props(button).onClick();});
      assert.deepEqual(view.calls,[expectedChain(sample)],'advisory availability/role supplies no new confirmation, args or gate');
      assert.equal(JSON.stringify(sample.hostStatus),before);
    } finally {await view.close();}
  }
});

test('readiness, runnable selection and an in-flight original action keep the existing button and plain-End conditions',async () => {
  const sample = actualPacket().cases[0],pending = Promise.withResolvers();
  const view = await mount(sample,() => pending.promise);
  let action;
  try {
    const starting = structuredClone(sample.hostStatus);starting.state = 'starting';
    await view.render(starting);
    assert.equal(props(chainButton(articleFor(view.container,sample.currentRun))).disabled,true);
    const notRunnable = structuredClone(sample.hostStatus);selectionFor(notRunnable,sample.threadId).runnable = false;
    await view.render(notRunnable);
    assert.equal(props(chainButton(articleFor(view.container,sample.currentRun))).disabled,true);
    assert.ok(labelled(articleFor(view.container,sample.currentRun),'Selected workflow for the next run'),'the disabled choice still identifies the selected candidate');
    assert.deepEqual(view.calls,[]);
    await view.render(sample.hostStatus);
    await React.act(() => {action = props(chainButton(articleFor(view.container,sample.currentRun))).onClick();});
    const article = articleFor(view.container,sample.currentRun);
    assert.equal(props(chainButton(article)).disabled,true,'the original action sets busy');
    assert.equal(props(nodes(article,'button').find(node => node.textContent === 'End run')).disabled,true);
    assert.ok(labelled(article,'Selected workflow for the next run'));
    assert.deepEqual(view.calls,[expectedChain(sample)]);
    await React.act(async () => {pending.resolve({state:'synthetic original action returned'});await action;});
    assert.equal(!!props(chainButton(articleFor(view.container,sample.currentRun))).disabled,false);
    assert.equal(view.calls.length,1);
  } finally {pending.resolve({});if (action) await React.act(async () => {await action;});await view.close();}
});

test('the existing source-context guard refuses a stale displayed choice rather than manufacturing or retargeting the chain context',async () => {
  const sample = actualPacket().cases[0],view = await mount(sample);
  try {
    const switchedHost = structuredClone(sample.hostStatus);switchedHost.workflowRoot.context.sourceRef = 'synthetic-replaced-source';
    await view.render(switchedHost,sample.hostStatus.workflowRoot);
    const button = chainButton(articleFor(view.container,sample.currentRun));
    assert.equal(!!props(button).disabled,false,'no new presentation gate is introduced');
    await React.act(async () => {await props(button).onClick();});
    assert.deepEqual(view.calls,[],'the existing workflowArguments guard refuses before dispatch');
    assert.ok(view.container.textContent.includes('Workflow source or chat changed; refresh the displayed choice before acting'));
    await view.render(sample.hostStatus);
    await React.act(async () => {await props(chainButton(articleFor(view.container,sample.currentRun))).onClick();});
    assert.deepEqual(view.calls,[expectedChain(sample)]);
  } finally {await view.close();}
});
