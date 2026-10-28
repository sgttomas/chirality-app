import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import React from 'react';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {App} = loadSrc('App');
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
const buttons = container => container.querySelectorAll(node => node.localName === 'button');
const SEND = 'Record, then send original prepared text once';

function actualDispatchCases() {
  let output;
  if (process.env.CHIRALITY_WORKFLOW_SUPPLY_DISPATCH_DTO_LOG) output = readFileSync(process.env.CHIRALITY_WORKFLOW_SUPPLY_DISPATCH_DTO_LOG,'utf8');
  else {
    const result = spawnSync('cargo',['test','--offline','--locked','--lib','workflow_supply_dispatch','--','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:8*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);
    output = result.stdout;
  }
  const summary = Array.from(output.matchAll(/^test result: (ok|FAILED)\. (\d+) passed; (\d+) failed;/gm)).at(-1);
  assert.ok(summary?.[1] === 'ok' && Number(summary[2]) > 0 && Number(summary[3]) === 0,'actual Rust dispatch checks completed successfully');
  assert.match(output,/test .*workflow_supply_dispatch/);
  const marker = 'WORKFLOW_SUPPLY_DISPATCH_DTO:';
  const lines = output.split('\n').filter(line => line.includes(marker));
  assert.equal(lines.length,1,'one actual dispatch evidence packet');
  return JSON.parse(lines[0].slice(lines[0].indexOf(marker)+marker.length)).cases;
}

test('actual generated-copy refusal preserves original intent and publication state through an explicit successful retry', async () => {
  const cases = actualDispatchCases();
  assert.deepEqual(cases.map(source => source.prepublished).sort(),[false,true],'unpublished and already-published preparations are exercised');
  for (const source of cases) {
    const {prepared,refused,restored,error,result,originalText,afterRefusalText,afterRestoredText,nativeStarts} = source;
    assert.equal(afterRefusalText,originalText);
    assert.equal(afterRestoredText,originalText);
    assert.equal(createHash('sha256').update(originalText).digest('hex'),prepared.runText.text_identity.value);
    assert.deepEqual(refused.runText,prepared.runText);
    assert.deepEqual(restored.runText,prepared.runText);
    assert.equal(nativeStarts.refused,nativeStarts.before,'guard refusal precedes any native attempt');
    assert.equal(nativeStarts.restored,nativeStarts.before+1,'restored original intent is sent exactly once');
    assert.equal(refused.reference,prepared.reference);
    assert.equal(restored.reference,prepared.reference);
    assert.equal(refused.source,null);
    assert.equal(refused.status.sent,false);
    assert.equal(refused.status.supplied,'not supplied');
    assert.equal(refused.publication.state,source.prepublished ? 'selection and run_text recorded before send' : 'pending; not recorded','refusal does not hide records already published before the final guard');
    for (const field of ['selection','runText']) {
      const record = refused.status.records[field];
      assert.equal(record.reference,prepared.publication[field]);
      if (source.prepublished) assert.equal(record.state,'recorded (resolves)');
      else {
        assert.ok(['not recorded','not confirmed'].includes(record.state),'a refused read cannot acquire a recorded claim');
        if (record.state === 'not confirmed') assert.ok(record.limit,'unconfirmed readback retains its actual cause');
      }
    }
    assert.ok(restored.source,'actual native attempt has its original source evidence');

    let current = prepared,sendPresses = 0;
    const calls = [];
    const idle = installIdleNativeWaiting(async (name,args) => {
      calls.push([name,args]);
      if (name === 'host_status') return {state:'ready',generation:prepared.generation,threads:[],workflowRoot:{runs:[current]}};
      if (name === 'decision_view') return {rows:[]};
      if (name === 'native_confirmation_content') return [];
      if (name === 'workflow_send_run') {
        assert.deepEqual(args,{runRef:prepared.reference});
        sendPresses += 1;
        if (sendPresses === 1) {current = refused;throw error;}
        assert.equal(sendPresses,2,'there is only one original retry');
        current = restored;
        return result;
      }
      throw Error(`Unexpected command: ${name}`);
    });
    const container = document.createElement('div');
    document.body.appendChild(container);
    const root = createRoot(container);
    const send = () => buttons(container).find(node => node.textContent === SEND);
    const runArticle = () => container.querySelectorAll(node => node.localName === 'article' && node.querySelectorAll(child => child.localName === 'h3' && child.textContent === prepared.reference).length)[0];
    const evidence = () => {
      const detail = runArticle().querySelectorAll(node => node.localName === 'details' && node.querySelectorAll(child => child.localName === 'summary' && child.textContent === 'Complete run evidence (paths shown as text)').length)[0];
      return JSON.parse(detail.querySelectorAll(node => node.localName === 'pre')[0].textContent);
    };
    const actions = () => calls.filter(([name]) => !['host_status','decision_view','native_confirmation_content'].includes(name));
    const press = async () => {assert.ok(send());assert.equal(props(send()).disabled,false);await React.act(async () => {await props(send()).onClick();});};
    try {
      await React.act(() => root.render(React.createElement(App)));
      assert.deepEqual(actions(),[],'rendering the preparation dispatches and repairs nothing');
      assert.equal(props(send()).disabled,false);
      assert.ok(runArticle().textContent.includes(prepared.runText.text_identity.value));
      await press();
      assert.deepEqual(actions(),[['workflow_send_run',{runRef:prepared.reference}]]);
      assert.ok(container.textContent.includes(error),'the actual host refusal reaches the existing alert/status');
      // Exercise the existing read-only host refresh after an error; it cannot
      // prepare a replacement, restore files or retry the native send.
      document.visibilityState = 'visible';
      const shown = document.listeners.find(listener => listener.type === 'visibilitychange').listener;
      await React.act(async () => {shown();await new Promise(resolve => setTimeout(resolve,0));});
      assert.equal(actions().length,1);
      assert.ok(runArticle().textContent.includes(`Records: ${refused.publication.state}`));
      assert.ok(runArticle().textContent.includes(`Send: ${refused.status.state}`));
      assert.match(runArticle().textContent,/Supplied: not supplied\. Adoption: unknown/);
      assert.ok(runArticle().textContent.includes(refused.status.limit));
      assert.ok(runArticle().textContent.includes(prepared.runText.text_identity.value),'refusal preserves the original prepared text identity');
      assert.deepEqual(evidence().runText,prepared.runText,'the original supporting-files line and text identity remain retained');
      assert.deepEqual(evidence().status.records,refused.status.records,'record readback limits remain visible in the existing source evidence');
      assert.equal(props(send()).disabled,false,'the unattempted original intent remains usable after its copy is restored');
      await press();
      assert.deepEqual(actions(),[['workflow_send_run',{runRef:prepared.reference}],['workflow_send_run',{runRef:prepared.reference}]],'retry never silently prepares another run or invokes a file repair');
      assert.equal(props(send()).disabled,true,'an admitted native attempt cannot be resent through this control');
      assert.ok(runArticle().textContent.includes(prepared.runText.text_identity.value));
      assert.match(runArticle().textContent,/Adoption: unknown/,'native dispatch does not claim provider adoption');
    } finally {
      const renderedText = container.textContent;
      await React.act(() => root.unmount());
      document.body.removeChild(container);
      idle.restore(renderedText);
    }
  }
});
