import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import React from 'react';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {App,ConversationPanel} = loadSrc('App');
const nodes = (container,tag) => container.querySelectorAll(node => node.localName === tag);
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
const labelled = (container,label) => container.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const conversation = container => container.querySelectorAll(node => node.getAttribute('id') === 'conversation')[0];
const composer = container => nodes(conversation(container),'textarea')[0];
const button = (container,label) => nodes(conversation(container),'button').find(node => node.textContent === label);
const alerts = container => conversation(container).querySelectorAll(node => node.getAttribute('role') === 'alert').map(node => node.textContent);
const outcome = container => labelled(container,'Attachment submission outcome');
const sendLabel = 'Send text and ordered attachments';
const steerLabel = 'Steer current turn with ordered attachments';
const ack = 'Matching attachment native acknowledgment observed; provider uptake and completion remain unestablished.';
const sha = value => createHash('sha256').update(value).digest('hex');
function freeze(value) {
  if (value && typeof value === 'object') {Object.values(value).forEach(freeze);Object.freeze(value);}
  return value;
}
let packet;
function actualPacket() {
  if (packet) return packet;
  const producer = 'hosting::conversation_transport_tests::attachment_outcome_tests::attachment_outcome_actual_send_steer_refusal_and_pending_late_dto';
  let output;
  if (process.env.CHIRALITY_ATTACHMENT_OUTCOME_DTO_LOG) output = readFileSync(process.env.CHIRALITY_ATTACHMENT_OUTCOME_DTO_LOG,'utf8');
  else {
    const result = spawnSync('cargo',['test','--offline','--locked','--lib',producer,'--','--exact','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:16*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);output = result.stdout;
  }
  assert.match(output,/test result: ok\. 1 passed; 0 failed;/);
  assert.ok(output.includes(`test ${producer}`));
  const marker = 'ATTACHMENT_OUTCOME_DTO:';
  const rows = output.split('\n').filter(line => line.includes(marker));
  assert.equal(rows.length,1,'one unchanged actual native producer packet');
  const raw = rows[0].slice(rows[0].indexOf(marker)+marker.length);
  packet = freeze(JSON.parse(raw));
  assert.deepEqual(packet.cases.map(sample => sample.case),['send','steer','changed-file','native-error','malformed-reply','pending-then-late-ack']);
  console.log('ATTACHMENT_CONSUMER_INPUT:',JSON.stringify({packetSha256:sha(raw),standing:packet.standing,
    limit:'Mounted App IPC replay only. Actual Host snapshots and command results are unchanged; no AppState/platform wrapper, native App, supplier or provider witness. Controlled read failures and timing variants are frontend controls.'}));
  return packet;
}
const sampleFor = name => actualPacket().cases.find(sample => sample.case === name);
function selectionView(container) {
  const panel = nodes(container,'h2').find(node => node.textContent === 'Selected text attachments').parentNode;
  const articles = nodes(panel,'article');
  return {
    refs:articles.filter(node => /^\d+\. /.test(nodes(node,'h3')[0]?.textContent ?? '')).map(node => JSON.parse(nodes(node,'pre')[0].textContent).selectionRef),
    submissions:articles.filter(node => (nodes(node,'h3')[0]?.textContent ?? '').startsWith('Submission ')).map(node => JSON.parse(nodes(node,'pre')[0].textContent)),
  };
}
async function mountApp(sample,{refreshFails = false,deferView = false,observerSnapshot = sample.afterHostStatus} = {}) {
  const packetBefore = JSON.stringify(actualPacket()),calls = [],unexpected = [];
  const nativeGate = Promise.withResolvers(),viewGate = Promise.withResolvers();
  let invoked = false,postRead = false,late = false,pollSnapshot = null,pending;
  const observerError = `Controlled host_status observation failed after ${sample.case}`;
  const idle = installIdleNativeWaiting(async (command,args) => {
    calls.push([command,structuredClone(args)]);
    if (command === 'host_status') {
      if (invoked && !postRead && nativeGate.settled) {
        postRead = true;
        if (deferView) await viewGate.promise;
        if (refreshFails) throw Error(observerError);
        return observerSnapshot;
      }
      return pollSnapshot ?? (late ? sample.lateObservation.afterHostStatus : invoked && nativeGate.settled ? sample.afterHostStatus : sample.beforeHostStatus);
    }
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    if (command === sample.command) {
      assert.deepEqual(args,sample.args,'unchanged actual generation/thread/expected turn/text/owner/revision/ordered refs');
      assert.equal(invoked,false,'one explicit attachment dispatch');invoked = true;
      await nativeGate.promise;
      if (sample.resultKind === 'Ok') return sample.nativeValue;
      assert.equal(sample.resultKind,'Err');throw sample.nativeError;
    }
    unexpected.push(command);throw Error(`Unexpected IPC: ${command}`);
  });
  const container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
  const view = {container,calls,observerError,
    async start() {
      const row = sample.beforeHostStatus.threads.find(row => row.threadId === sample.args.threadId && JSON.stringify(row.generation) === JSON.stringify(sample.args.generation));
      assert.ok(row);
      await React.act(() => props(nodes(conversation(container),'select')[0]).onChange({target:{value:JSON.stringify([row.generation,row.threadId])}}));
      await React.act(() => props(composer(container)).onChange({target:{value:sample.args.text}}));
      assert.deepEqual(selectionView(container).refs,sample.args.selectionRefs);
      assert.equal(calls.filter(([command]) => command === sample.command).length,0,'mount/select/type has no attachment effect');
      const target = button(container,sample.args.expectedTurnId === null ? sendLabel : steerLabel);
      assert.equal(!!props(target).disabled,false);
      this.actionStart = calls.length;
      await React.act(() => {pending = props(target).onClick();});
      assert.equal(props(composer(container)).value,sample.args.text);
      for (const control of [composer(container),nodes(conversation(container),'select')[0],button(container,sendLabel),button(container,steerLabel)]) assert.equal(!!props(control).disabled,true);
    },
    async releaseNative() {await React.act(async () => {nativeGate.settled = true;nativeGate.resolve();if (!deferView) this.returned = await pending;});},
    async releaseView() {await React.act(async () => {viewGate.resolve();this.returned = await pending;});},
    async poll(t,snapshot) {pollSnapshot = snapshot;await React.act(async () => {t.mock.timers.tick(1000);});},
    async late(t) {late = true;await React.act(async () => {t.mock.timers.tick(1000);});},
    assertOriginalIdentity() {
      const text = outcome(container).textContent,request = sample.args;
      for (const value of [request.threadId,...Object.values(request.generation),request.ownerRef,String(request.listRevision),...request.selectionRefs]) assert.ok(text.includes(String(value)),String(value));
      if (request.expectedTurnId !== null) assert.ok(text.includes(`expected turn ${request.expectedTurnId}`));
      assert.deepEqual(nodes(outcome(container),'li').map(node => node.textContent),request.selectionRefs);
    },
    async close() {
      nativeGate.resolve();viewGate.resolve();
      if (pending) await React.act(async () => {await pending;});
      assert.deepEqual(unexpected,[]);idle.assertClean(container);
      const renderedText = container.textContent;
      await React.act(async () => {root.unmount();});document.body.removeChild(container);idle.restore(renderedText);
      assert.equal(idle.calls.filter(call => call.command === 'plugin:event|listen').length,1);
      assert.equal(idle.calls.filter(call => call.command === 'plugin:event|unlisten').length,1);
      assert.equal(JSON.stringify(actualPacket()),packetBefore,'neither the consumer nor harness mutates producer inputs');
    },
  };
  try {await React.act(async () => {root.render(React.createElement(App));});idle.assertClean(container);return view;}
  catch (e) {await view.close();throw e;}
}

test('actual acknowledged Send and Steer retain native completion independently of the following Host read',async t => {
  t.mock.timers.enable({apis:['setInterval']});
  for (const name of ['send','steer']) for (const refreshFails of [false,true]) await t.test(`${name}: view ${refreshFails ? 'unavailable' : 'available'}`,async () => {
    const sample = sampleFor(name),view = await mountApp(sample,{refreshFails});
    try {
      await view.start();await view.releaseNative();
      assert.equal(view.returned,sample.nativeValue,'the actual native Value reaches the leaf unchanged, without a UI envelope');
      assert.equal(props(composer(view.container)).value,'','matching acknowledgment clears the submitted text despite a read failure');
      assert.ok(outcome(view.container).textContent.includes(ack));view.assertOriginalIdentity();
      assert.equal(!!props(composer(view.container)).disabled,false);
      assert.equal(!!props(button(view.container,sendLabel)).disabled,false,'ordinary explicit new Send stays available');
      const expected = refreshFails ? sample.beforeHostStatus : sample.afterHostStatus;
      assert.deepEqual(selectionView(view.container),{refs:expected.attachmentSelections.selections.map(row => row.selection.selectionRef),submissions:expected.attachmentSelections.submissions});
      assert.equal(!!props(button(view.container,steerLabel)).disabled,!(expected.steeringTargets ?? []).some(row => row.target));
      if (refreshFails) {
        assert.equal(alerts(view.container).length,1);assert.ok(alerts(view.container)[0].includes(view.observerError));
        assert.ok(alerts(view.container)[0].includes('command outcome above is unchanged'));
      } else assert.deepEqual(alerts(view.container),[]);
      assert.deepEqual(view.calls.slice(view.actionStart).map(([command]) => command),[sample.command,'host_status']);
      console.log('ATTACHMENT_FIXED_CONSUMER:',JSON.stringify({case:name,refreshFails,nativeValueSha256:sha(JSON.stringify(view.returned)),args:view.calls.find(([command]) => command === sample.command)[1],composerText:props(composer(view.container)).value,alerts:alerts(view.container),dispatchCount:1}));
    } finally {await view.close();}
  });
});

test('actual native refusal, error, malformed reply and pending error survive a separate view failure',async t => {
  t.mock.timers.enable({apis:['setInterval']});
  for (const name of ['changed-file','native-error','malformed-reply','pending-then-late-ack']) await t.test(name,async () => {
    const sample = sampleFor(name),view = await mountApp(sample,{refreshFails:true});
    try {
      await view.start();await view.releaseNative();
      assert.equal(view.returned,undefined);
      assert.equal(props(composer(view.container)).value,sample.args.text);
      assert.deepEqual(alerts(view.container).slice(0,1),[`${sample.nativeError} No automatic retry.`]);
      assert.equal(alerts(view.container).length,2);assert.ok(alerts(view.container)[1].includes(view.observerError));
      assert.ok(!outcome(view.container).textContent.includes(ack));view.assertOriginalIdentity();
      assert.equal(!!props(button(view.container,sendLabel)).disabled,false);
      assert.equal(!!props(composer(view.container)).disabled,false);
      assert.deepEqual(view.calls.slice(view.actionStart).map(([command]) => command),[sample.command,'host_status']);
    } finally {await view.close();}
  });
});

test('actual pending Err remains the command result when a later source observation finds its acknowledgment',async t => {
  t.mock.timers.enable({apis:['setInterval']});
  const sample = sampleFor('pending-then-late-ack'),view = await mountApp(sample);
  try {
    await view.start();await view.releaseNative();
    const originalAlerts = alerts(view.container);
    assert.deepEqual(originalAlerts,[`${sample.nativeError} No automatic retry.`]);
    await view.late(t);
    assert.deepEqual(selectionView(view.container).submissions,sample.lateObservation.afterHostStatus.attachmentSelections.submissions);
    assert.equal(selectionView(view.container).submissions[0].outcome.resolution.nativeReplyObserved,true);
    assert.deepEqual(alerts(view.container),originalAlerts);
    assert.equal(props(composer(view.container)).value,sample.args.text);
    assert.ok(!outcome(view.container).textContent.includes(ack),'late evidence does not rewrite the original Err as a command acknowledgment');
    assert.equal(view.calls.filter(([command]) => command === sample.command).length,1);
  } finally {await view.close();}
});

test('derived source timing control: a pending original outcome cannot clear another source or apply its old view',async t => {
  // Frontend timing control using two actual snapshots, not a new native scenario.
  t.mock.timers.enable({apis:['setInterval']});
  const sample = sampleFor('send'),other = sampleFor('steer').beforeHostStatus;
  assert.notDeepEqual(other.generation,sample.args.generation);
  const view = await mountApp(sample,{deferView:true});
  try {
    await view.start();await view.poll(t,other);
    assert.ok(conversation(view.container).textContent.includes('Selected conversation is no longer available'));
    await view.releaseNative();
    assert.equal(props(composer(view.container)).value,sample.args.text,'original acknowledgment does not clear a different current source');
    assert.ok(outcome(view.container).textContent.includes(ack));
    await view.releaseView();
    assert.ok(alerts(view.container).some(text => text.includes('current source changed')));
    assert.deepEqual(selectionView(view.container).refs,other.attachmentSelections.selections.map(row => row.selection.selectionRef),'old read cannot replace the current source selection');
    view.assertOriginalIdentity();
    assert.equal(view.calls.filter(([command]) => command === sample.command).length,1);
  } finally {await view.close();}
});

test('derived delayed-read control: a newer same-source view is not overwritten by the original observer',async t => {
  // Deliberately delayed/stale read, using unchanged before/after producer
  // snapshots. This is an observer timing control, not another native result.
  t.mock.timers.enable({apis:['setInterval']});
  const sample = sampleFor('send'),view = await mountApp(sample,{deferView:true,observerSnapshot:sample.beforeHostStatus});
  try {
    await view.start();await view.releaseNative();
    assert.equal(props(composer(view.container)).value,'');
    await view.poll(t,sample.afterHostStatus);await view.releaseView();
    assert.ok(alerts(view.container).some(text => text.includes('newer view arrived')));
    assert.deepEqual(selectionView(view.container).submissions,sample.afterHostStatus.attachmentSelections.submissions);
    assert.ok(outcome(view.container).textContent.includes(ack));view.assertOriginalIdentity();
    assert.equal(view.calls.filter(([command]) => command === sample.command).length,1);
  } finally {await view.close();}
});

test('standalone ConversationPanel preserves its raw return and optional legacy observer contract',async () => {
  const sample = sampleFor('send'),request = sample.args,calls = [],gate = Promise.withResolvers();
  const container = document.createElement('div');document.body.appendChild(container);const root = createRoot(container);
  const noop = async () => {};
  const panelProps = {host:sample.beforeHostStatus,threadKey:JSON.stringify([request.generation,request.threadId]),setThreadKey:() => {},answer:noop,runAct:noop,send:noop,steer:noop,interrupt:noop,checkPlanMode:noop,codexBusy:false,
    submitAttachments:async (...args) => {calls.push(args);return sample.nativeValue;},observeAttachmentView:async () => {await gate.promise;}};
  let pending;
  try {
    await React.act(() => root.render(React.createElement(ConversationPanel,panelProps)));
    await React.act(() => props(composer(container)).onChange({target:{value:request.text}}));
    await React.act(async () => {pending = props(button(container,sendLabel)).onClick();});
    assert.equal(props(composer(container)).value,'');
    assert.equal(!!props(composer(container)).disabled,true,'existing busy condition prevents edits during the observer');
    await React.act(async () => {gate.resolve();assert.equal(await pending,sample.nativeValue);});
    await React.act(() => props(composer(container)).onChange({target:{value:'Newer person draft'}}));
    await React.act(() => root.render(React.createElement(ConversationPanel,{...panelProps,host:sample.afterHostStatus})));
    assert.equal(props(composer(container)).value,'Newer person draft');
    assert.deepEqual(calls,[[request.generation,request.threadId,request.expectedTurnId,request.text,request.ownerRef,request.listRevision,request.selectionRefs]]);
    // Existing standalone fixtures need not provide a read observer or a Value.
    await React.act(() => root.render(React.createElement(ConversationPanel,{...panelProps,submitAttachments:noop,observeAttachmentView:undefined})));
    await React.act(async () => {await props(button(container,sendLabel)).onClick();});
    assert.equal(props(composer(container)).value,'');
  } finally {gate.resolve();if (pending) await pending;await React.act(() => root.unmount());document.body.removeChild(container);}
});
