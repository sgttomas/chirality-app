import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
import test from 'node:test';
import assert from 'node:assert/strict';
import React from 'react';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {App} = loadSrc('App');
const {ArrivalRecord} = loadSrc('RunPanel');
const {FileActPanel} = loadSrc('FileActPanel');
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
const nodes = (container,tag) => container.querySelectorAll(node => node.localName === tag);
const button = (container,label) => nodes(container,'button').find(node => node.textContent === label);
async function press(container,label) {
  const control = button(container,label);
  assert.ok(control,label);
  assert.equal(props(control).disabled,false,label);
  await React.act(async () => {await props(control).onClick();});
}
function mount(Component,initial) {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  return {container,show: async (next = initial) => React.act(() => root.render(React.createElement(Component,next))),
    close: async () => React.act(() => root.unmount())};
}
const generation = {appSession:'synthetic-arrival-session',home:'synthetic-arrival-home',spawnCounter:1};
function fixture(kind = 'A4') {
  const arrival = {kind:'checkpoint_arrival',recordId:`rec:synthetic:arrival-${kind}`,written:true,body:{checkpoint:`CP-${kind}`,arrivalOrdinal:1,
    requiredAct:kind,subjectClass:'named output',scope:'one reviewed output',purpose:'synthetic review purpose',
    referents:[{subject:'output report: file output.txt',content:{method:'sha256-exact-bytes/0.1',value:'content-for-review'}}],
    event:{ref:'item:synthetic/file',evidencedTime:{value:'2026-10-18T00:00:00Z',source:'app_observation_time'}},requestObservation:{state:'not yet observed'}}};
  const listed = {kind:'checkpoint_listed',recordId:`listed-${kind}`,written:true,body:{checkpoint:`CP-${kind}`,evaluability:{status:'evaluable',reason:'synthetic file observation'}}};
  const declaration = {raw:{},reading:'recognized',categories:{checkpoints:'recognized'},elements:{checkpoints:[{reading:'recognized',value:{name:`CP-${kind}`,required_act:kind,
    actor:kind === 'A7' ? 'the_accountable_professional' : 'the_person',subject:{class:'named_output',output:'report'},scope:arrival.body.scope,purpose:arrival.body.purpose,
    reached_when:{kind:'output_produced',output:'report'},expected_act_evidence:{capturing_surface:'app_act_control'}}}]}};
  const run = {reference:`run:synthetic:${kind}`,workflow:{name:'review-report',origin:'project',revision:'synthetic-revision'},conversation:'synthetic-chat',home:generation.home,generation,
    lifecycle:{state:"open (live); only the person's explicit end ends it",records:[listed,arrival]},
    compatibility:[{occasionLabel:'run start',preparation:{declaration}}],fileActEntries:{[arrival.recordId]:{state:'candidate',reason:'Held live single-file arrival; current source is rechecked on review.'}}};
  const preview = {reference:`offer:synthetic:${kind}`,byteLength:14,utf8:'reviewed bytes',hex:'7265766965776564206279746573',previewStanding:'exact frozen bytes; selection and preview are not act evidence',offer:{
    actKind:kind,wording:{A4:'mark checked',A6:'approve (engineering approval)',A7:'rely (professional reliance)'}[kind],subject:{ref:'/synthetic/project/output.txt',contentIdentity:arrival.body.referents[0].content},
    scope:arrival.body.scope,purpose:arrival.body.purpose,actorRequirement:kind === 'A7' ? "the accountable professional (the person's own statement; not verified)" : 'the person',
    answers:{runId:run.reference,arrival:{checkpoint:arrival.body.checkpoint,arrivalOrdinal:1}}}};
  return {run,arrival,preview};
}

test('App arrival click opens only the host-resolved frozen review, with native confirmation separate', async () => {
  const {run,arrival,preview} = fixture();
  let snapshot = {state:'ready',generation,threads:[],workflowRoot:{runs:[run]}};
  const calls = [],scrolls = [];
  const previousFind = document.getElementById;
  document.getElementById = id => {
    const element = document.body.querySelectorAll(node => node.getAttribute('id') === id)[0];
    if (element) element.scrollIntoView = () => scrolls.push(id);
    return element;
  };
  const idle = installIdleNativeWaiting(async (name,args) => {
    calls.push([name,args]);
    if (name === 'host_status') return snapshot;
    if (name === 'decision_view') return {rows:[]};
    if (name === 'native_confirmation_content') return [];
    if (name === 'file_act_open_arrival') return preview;
    if (name === 'file_act_confirm') return {state:'original native capture recorded',recorded:true,captureId:'cap:synthetic:original'};
    throw Error(`Unexpected command: ${name}`);
  });
  const view = mount(App,{});
  const actions = () => calls.filter(([name]) => name.startsWith('file_act_') || /answer|submit|conversation_send|steer/.test(name));
  try {
    await view.show();
    assert.deepEqual(actions(),[],'mount does not compose, confirm or settle anything');
    assert.deepEqual(scrolls,[]);
    await view.show();
    assert.deepEqual(actions(),[],'rerender does not open a review');
    await press(view.container,'Review file for this arrival…');
    assert.deepEqual(actions(),[['file_act_open_arrival',{runRef:run.reference,arrivalRecordId:arrival.recordId}]],'renderer sends only host-owned identities');
    assert.deepEqual(scrolls,['file-acts'],'only the explicit review click navigates to its returned offer');
    const fileSection = document.getElementById('file-acts');
    assert.match(fileSection.textContent,/Origin: selected arrival/);
    assert.ok(fileSection.textContent.includes(run.reference));
    assert.ok(fileSection.textContent.includes(arrival.body.checkpoint));
    assert.match(fileSection.textContent,/Kind: A4/);
    assert.ok(fileSection.textContent.includes(preview.offer.subject.ref));
    assert.ok(fileSection.textContent.includes(preview.offer.subject.contentIdentity.value));
    assert.match(fileSection.textContent,/standing-selection fields do not edit it/);
    snapshot = {...snapshot,workflowRoot:{runs:[{...run,fileActEntries:{[arrival.recordId]:{state:'unavailable',reason:'Original source is no longer current.'}}}]}};
    document.visibilityState = 'visible';
    const shown = document.listeners.find(listener => listener.type === 'visibilitychange').listener;
    await React.act(async () => {shown();await new Promise(resolve => setTimeout(resolve,0));});
    assert.equal(actions().length,1,'snapshot changes do not replace or confirm the frozen offer');
    assert.deepEqual(scrolls,['file-acts']);
    assert.equal(button(view.container,'Review file for this arrival…'),undefined);
    assert.match(view.container.textContent,/Arrival file review unavailable: Original source is no longer current/);
    await press(fileSection,'Review native act / decline / cancel…');
    assert.deepEqual(actions()[1],['file_act_confirm',{reference:preview.reference}]);
    assert.match(fileSection.textContent,/original native capture recorded/);
    assert.equal(props(button(fileSection,'Review native act / decline / cancel…')).disabled,true);
  } finally {
    const renderedText = view.container.textContent;
    await view.close();
    idle.restore(renderedText);
    document.getElementById = previousFind;
  }
});

test('host refusal never becomes a standing offer, and retained offers continue only their original reference', async () => {
  const original = fixture('A7').preview;
  const controlRef = React.createRef();
  const calls = [];
  let selection = original;
  const command = async (name,args) => {
    calls.push([name,args]);
    if (name === 'file_act_open_arrival') {
      if (args.arrivalRecordId === 'refused-arrival') throw Error('Source changed; review is unavailable');
      return selection;
    }
    if (name === 'file_act_confirm') return {state:'original capture saved; record pending',recorded:false,captureId:'cap:synthetic:pending'};
    if (name === 'file_act_continue') return {state:'original record saved',recorded:true,captureId:'cap:synthetic:pending'};
    if (name === 'file_act_select') return selection;
    throw Error(`Unexpected command: ${name}`);
  };
  const view = mount(FileActPanel,{command,controlRef});
  try {
    await view.show();
    await React.act(async () => {await controlRef.current.openArrival('original-run','original-arrival');});
    await press(view.container,'Review native act / decline / cancel…');
    await React.act(async () => {await controlRef.current.openArrival('other-run','refused-arrival');});
    assert.match(view.container.textContent,/Arrival file review unavailable; no new offer opened/);
    assert.equal(button(view.container,'Review native act / decline / cancel…'),undefined,'refusal does not leave the prior offer looking like the new review');
    await press(view.container,`Show original offer ${original.reference}`);
    assert.match(view.container.textContent,/original capture saved; record pending/);
    assert.equal(props(button(view.container,'Review native act / decline / cancel…')).disabled,true);
    await press(view.container,'Continue this original capture/record only');
    assert.deepEqual(calls.at(-1),['file_act_continue',{reference:original.reference}]);
    selection = {...fixture('A4').preview,reference:'offer:synthetic:standing',offer:{...fixture('A4').preview.offer,answers:{standing:'no arrival: a standing act (RC-6)'}}};
    const inputs = nodes(view.container,'input');
    await React.act(() => {props(inputs[0]).onChange({target:{value:'explicit standing scope'}});props(inputs[1]).onChange({target:{value:'explicit standing purpose'}});});
    await press(view.container,'Select file and freeze preview…');
    assert.match(view.container.textContent,/Origin: standing file selection\. No arrival or request is associated/);
    assert.deepEqual(calls.at(-1),['file_act_select',{kind:'A4',scope:'explicit standing scope',purpose:'explicit standing purpose'}]);
    assert.equal(calls.filter(([name]) => name === 'file_act_confirm').length,1);
  } finally {await view.close();}
});

test('historical, missing and host-refused arrival entries display their limits without an active review control', async () => {
  const {run,arrival} = fixture();
  const calls = [];
  const openFileAct = async (...args) => {calls.push(args);};
  for (const [fileActEntry,runRef,reason] of [
    [undefined,undefined,'Historical or reopened arrival'],
    [undefined,run.reference,'No current file-act entry was supplied'],
    [{state:'unavailable',reason:'Message, host or multiple-subject arrival has no single App file.'},run.reference,'Message, host or multiple-subject arrival'],
  ]) {
    const view = mount(ArrivalRecord,{arrival,all:[arrival],runRef,fileActEntry,openFileAct});
    try {
      await view.show();
      assert.equal(button(view.container,'Review file for this arrival…'),undefined);
      assert.ok(view.container.textContent.includes(reason));
      assert.deepEqual(calls,[]);
    } finally {await view.close();}
  }
});

test('an unresolved arrival review disables other rows and standing selection and retains the admitted original offer', async () => {
  const first = fixture('A4'),second = fixture('A6');
  const declaration = first.run.compatibility[0].preparation.declaration;
  const run = {...first.run,lifecycle:{...first.run.lifecycle,records:[...first.run.lifecycle.records,...second.run.lifecycle.records]},
    compatibility:[{preparation:{declaration:{...declaration,elements:{checkpoints:[...declaration.elements.checkpoints,...second.run.compatibility[0].preparation.declaration.elements.checkpoints]}}}}],
    fileActEntries:{...first.run.fileActEntries,...second.run.fileActEntries}};
  const snapshot = {state:'ready',generation,threads:[],workflowRoot:{runs:[run]}};
  const calls = [],pending = Promise.withResolvers();
  const previousFind = document.getElementById;
  document.getElementById = id => document.body.querySelectorAll(node => node.getAttribute('id') === id)[0];
  const idle = installIdleNativeWaiting(async (name,args) => {
    calls.push([name,args]);
    if (name === 'host_status') return snapshot;
    if (name === 'decision_view') return {rows:[]};
    if (name === 'native_confirmation_content') return [];
    if (name === 'file_act_open_arrival') return pending.promise;
    throw Error(`Unexpected command: ${name}`);
  });
  const view = mount(App,{});
  let firstOperation;
  try {
    await view.show();
    const section = document.getElementById('file-acts');
    const inputs = nodes(section,'input');
    await React.act(() => {props(inputs[0]).onChange({target:{value:'explicit scope'}});props(inputs[1]).onChange({target:{value:'explicit purpose'}});});
    const entries = nodes(view.container,'button').filter(node => node.textContent === 'Review file for this arrival…');
    assert.equal(entries.length,2);
    await React.act(() => {firstOperation = props(entries[0]).onClick();});
    assert.ok(entries.every(node => props(node).disabled),'pending shared review disables every arrival entry');
    const standing = button(section,'Select file and freeze preview…');
    assert.equal(props(standing).disabled,true);
    // Exercise the original event callbacks as well as their disabled display;
    // the panel's synchronous guard also covers clicks queued before a render.
    await React.act(async () => {await props(entries[1]).onClick();await props(standing).onClick();});
    assert.deepEqual(calls.filter(([name]) => name.startsWith('file_act_')),[['file_act_open_arrival',{runRef:first.run.reference,arrivalRecordId:first.arrival.recordId}]]);
    await React.act(async () => {pending.resolve(first.preview);await firstOperation;});
    assert.match(section.textContent,/Frozen offer: mark checked/);
    assert.ok(section.textContent.includes(first.arrival.body.checkpoint));
    assert.ok(!section.textContent.includes(second.arrival.body.checkpoint),'later row cannot relabel the returned original preview');
    assert.equal(props(button(section,'Review native act / decline / cancel…')).disabled,false,'the native confirmation remains a separate available press');
  } finally {
    pending.resolve(first.preview);
    if (firstOperation) await firstOperation;
    const renderedText = view.container.textContent;
    await view.close();
    idle.restore(renderedText);
    document.getElementById = previousFind;
  }
});

test('actual Rust arrival previews and capture records pass through the mounted App for each file-act kind', async () => {
  let output;
  if (process.env.CHIRALITY_FILE_ACT_ARRIVAL_DTO_LOG) output = readFileSync(process.env.CHIRALITY_FILE_ACT_ARRIVAL_DTO_LOG,'utf8');
  else {
    const result = spawnSync('cargo',['test','--offline','--locked','--lib','file_act_arrival','--','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:8*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);
    output = result.stdout;
  }
  const summary = Array.from(output.matchAll(/^test result: (ok|FAILED)\. (\d+) passed; (\d+) failed;/gm)).at(-1);
  assert.ok(summary?.[1] === 'ok' && Number(summary[2]) >= 1 && Number(summary[3]) === 0,'completed Rust test binary passed');
  assert.match(output,/test .*file_act_arrival/);
  const marker = 'FILE_ACT_ARRIVAL_DTO:';
  const lines = output.split('\n').filter(line => line.includes(marker));
  assert.equal(lines.length,1,'one actual production-path DTO packet');
  const packet = JSON.parse(lines[0].slice(lines[0].indexOf(marker)+marker.length));
  assert.deepEqual(packet.cases.map(row => row.preview.offer.actKind).sort(),['A4','A6','A7']);
  for (const source of packet.cases) {
    const {run,preview,result,read} = source;
    const arrival = run.lifecycle.records.find(row => row.kind === 'checkpoint_arrival' && row.body.checkpoint === preview.offer.answers.arrival.checkpoint && row.body.arrivalOrdinal === preview.offer.answers.arrival.arrivalOrdinal);
    assert.ok(arrival,'host run identifies the same arrival as its offer');
    assert.equal(run.fileActEntries[arrival.recordId].state,'candidate');
    assert.deepEqual(result.capture.answers,preview.offer.answers);
    assert.equal(result.record.runId,preview.offer.answers.runId);
    assert.deepEqual(result.record.body.relations.arrivalAnswered,preview.offer.answers.arrival);
    const calls = [],previousFind = document.getElementById;
    document.getElementById = id => document.body.querySelectorAll(node => node.getAttribute('id') === id)[0];
    const idle = installIdleNativeWaiting(async (name,args) => {
      calls.push([name,args]);
      if (name === 'host_status') return {state:'ready',generation:run.generation,threads:[],workflowRoot:{runs:[run]}};
      if (name === 'decision_view') return {rows:[]};
      if (name === 'native_confirmation_content') return [];
      if (name === 'file_act_open_arrival') return preview;
      if (name === 'file_act_confirm') return result;
      if (name === 'file_act_read') return read;
      throw Error(`Unexpected command: ${name}`);
    });
    const view = mount(App,{});
    const actions = () => calls.filter(([name]) => name.startsWith('file_act_') || /answer|submit|conversation_send|steer/.test(name));
    try {
      await view.show();
      assert.deepEqual(actions(),[]);
      await press(view.container,'Review file for this arrival…');
      assert.deepEqual(actions(),[['file_act_open_arrival',{runRef:run.reference,arrivalRecordId:arrival.recordId}]]);
      const section = document.getElementById('file-acts');
      assert.match(section.textContent,/Origin: selected arrival/);
      assert.ok(section.textContent.includes(preview.offer.answers.runId));
      assert.ok(section.textContent.includes(preview.offer.subject.contentIdentity.value));
      assert.ok(section.textContent.includes(preview.utf8));
      assert.ok(!section.textContent.includes('AC-7 recorded'),'a preview is not rendered as a completed act');
      await press(section,'Review native act / decline / cancel…');
      assert.deepEqual(actions()[1],['file_act_confirm',{reference:preview.reference}]);
      assert.ok(section.textContent.includes(result.state),'original actual native/record result remains visible');
      await press(section,'Read file-act log and current content');
      assert.deepEqual(actions()[2],['file_act_read',{}]);
      assert.ok(read.rows.some(row => row.recordId === result.record.recordId),'actual reader preserves the captured act record');
      assert.match(section.textContent,/Current content comparison/);
      assert.match(section.textContent,/Recorded lapse history/);
      assert.equal(actions().length,3,'no supplier answer, submission or implicit capture is introduced');
    } finally {
      const renderedText = view.container.textContent;
      await view.close();
      idle.restore(renderedText);
      document.getElementById = previousFind;
    }
  }
});
