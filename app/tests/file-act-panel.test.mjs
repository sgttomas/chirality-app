import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';
import React from 'react';
import {renderToStaticMarkup} from 'react-dom/server';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {readFileSync} from 'node:fs';

const document = installMiniDom();
const {createRoot} = await import('react-dom/client');
const {FileActPanel, FileActLapseHistory} = loadSrc('FileActPanel');
const props = node => node[Object.keys(node).find(key => key.startsWith('__reactProps$'))];
function mounted(command) {
  const container = document.createElement('div');
  document.body.appendChild(container);
  const root = createRoot(container);
  return {container,
    show: () => React.act(() => root.render(React.createElement(FileActPanel, {command}))),
    press: async label => {
      const button = container.querySelectorAll(node => node.localName === 'button' && node.textContent === label)[0];
      assert.ok(button, label);
      assert.equal(props(button).disabled, false, label);
      await React.act(async () => props(button).onClick());
    },
    close: () => React.act(() => root.unmount()),
  };
}

test('standing observation, read and held retry require explicit presses and never invoke capture', async () => {
  const calls = [];
  const original = {recordId:'observation:original',body:{state:'lapsed',time:'original observation time',c0:{method:'exact',value:'first'},c1:{method:'exact',value:'changed'}}};
  const view = mounted(async (name,args) => {
    calls.push([name,args]);
    return {rows:[],lapseObservation:{state:name === 'file_act_retry_lapses' ? 'saved original observation' : 'original observation not saved',
      pending:name === 'file_act_retry_lapses' ? [] : [original],limits:[]}};
  });
  try {
    await view.show();
    assert.deepEqual(calls, [], 'mounting the facility neither observes nor opens a confirmation');
    await view.press('Observe file-act content changes and save history');
    assert.match(view.container.textContent,/Save not established: 1 original content observation/);
    assert.match(view.container.textContent,/original observation time/);
    await view.press('Read file-act log and current content');
    await view.press('Retry saving held metadata only');
    assert.deepEqual(calls,[['file_act_observe_lapses',{}],['file_act_read',{}],['file_act_retry_lapses',{}]]);
    assert.match(view.container.textContent,/saved original observation/);
    assert.doesNotMatch(view.container.textContent,/Save not established:/);
    assert.equal(view.container.querySelectorAll(node => node.localName === 'button' && node.textContent === 'Retry saving held metadata only').length,0);
  } finally {await view.close();}
});

test('recorded intervals and return-to-content remain separate from limited source claims', () => {
  const c0 = {method:'exact-byte-method',value:'original-content'};
  const history = ['lapsed','lapsed (subject absent)','matches c0 again after observed lapse','unknown (unavailable)'].map((state,index) =>
    ({source:{log:'original observer log',seq:index+1},record:{recordId:`observation:${index}`,body:{state,time:`observed-${index}`,c0,c1:index===0 ? {method:c0.method,value:'changed-content'} : index===1 ? 'subject absent' : index===2 ? c0 : {notObtainable:true,reason:'source unavailable'}}}}));
  const html = renderToStaticMarkup(React.createElement(FileActLapseHistory,{row:{lapseHistoryClaims:history,
    lapseHistoryLimitedClaims:[{record:{recordId:'corrected-source',body:{state:'lapsed'}}}],lapseHistoryLimits:['corrected source cannot establish current interval']}}));
  for (const state of ['lapsed (subject absent)','matches c0 again after observed lapse','unknown (unavailable)']) assert.ok(html.includes(state),state);
  assert.match(html,/Content acted on \(c₀\): exact-byte-method: original-content/);
  assert.match(html,/observed observed-2/);
  assert.match(html,/History limit: corrected source cannot establish current interval/);
  assert.match(html,/Unresolved or historical lapse claims \(1\)/);
  assert.match(html,/does not perform or renew an act/);
  const limited = renderToStaticMarkup(React.createElement(FileActLapseHistory,{row:{lapseHistoryClaims:[],lapseHistoryLimitedClaims:[{record:{recordId:'conflict',body:{state:'lapsed'}}}]}}));
  assert.match(limited,/No resolved lapse observations recorded/);
  assert.doesNotMatch(limited,/<ol>/,'unresolved claims do not become an interval');
  const separate = renderToStaticMarkup(React.createElement(FileActLapseHistory,{row:{lapseHistoryClaims:[history[0],{...history[2],source:{log:'another run log',seq:1}}]}}));
  assert.equal((separate.match(/<ol>/g) ?? []).length,2,'source histories have separate recorded sequences');
  assert.match(separate,/No order is inferred between logs/);
});

test('actual standalone observer DTOs preserve cold intervals and distinguish original-save from disclosure failure', async () => {
  // A completed focused Rust run can be reused by its UI consumer. The normal
  // npm-test path still runs the real observer tests against the current source.
  let output;
  if (process.env.CHIRALITY_FILE_ACT_LAPSE_DTO_LOG) {
    output = readFileSync(process.env.CHIRALITY_FILE_ACT_LAPSE_DTO_LOG,'utf8');
  } else {
    const result = spawnSync('cargo',['test','--offline','--locked','--lib','file_act_lapse_tests::standalone_file_act_lapse_','--','--nocapture','--test-threads=1'],{
      cwd:fileURLToPath(new URL('../src-tauri/',import.meta.url)),encoding:'utf8',timeout:180000,maxBuffer:8*1024*1024,
      env:{...process.env,CHIRALITY_SKIP_CODEX:'1',CARGO_NET_OFFLINE:'true'},
    });
    assert.equal(result.status,0,result.error?.message ?? result.stderr+result.stdout);
    output = result.stdout;
  }
  // Broader Rust runs include nested fixture-process summaries. The last
  // result belongs to the consuming test binary, rather than a nested probe.
  const summary = Array.from(output.matchAll(/^test result: (ok|FAILED)\. (\d+) passed; (\d+) failed;/gm)).at(-1);
  assert.ok(summary?.[1] === 'ok' && Number(summary[2]) >= 3 && Number(summary[3]) === 0,'DTO output must contain a completed passing Rust run');
  for (const name of ['connected_and_cold_history_dto','pending_retry_keeps_original_metadata_dto','saved_observation_disclosure_failure_has_distinct_phase']) {
    assert.ok(output.includes(`test file_act_lapse_tests::standalone_file_act_lapse_${name} ... `),`completed run includes ${name}`);
  }
  const dto = marker => {
    const lines = output.split('\n').filter(line => line.includes(marker));
    assert.equal(lines.length,1,`one ${marker} from the actual Rust observer`);
    const [line] = lines;
    return JSON.parse(line.slice(line.indexOf(marker)+marker.length));
  };
  const cold = dto('FILE_ACT_LAPSE_DTO:');
  const row = cold.rows.find(row => row.kind === 'A4');
  assert.equal(row.lapseHistoryClaims.length,5);
  assert.match(row.comparison,/matches c0 again/);
  const history = renderToStaticMarkup(React.createElement(FileActLapseHistory,{row}));
  assert.match(history,/lapsed \(subject absent\)/);
  assert.match(history,/matches c0 again after observed lapse/);
  assert.match(history,/Content acted on \(c₀\)/);
  assert.match(history,/does not perform or renew an act/);
  const coldCalls = [];
  const coldView = mounted(async (name,args) => {coldCalls.push([name,args]);return cold;});
  try {
    await coldView.show();
    await coldView.press('Read file-act log and current content');
    assert.deepEqual(coldCalls,[['file_act_read',{}]]);
    const comparisons = coldView.container.querySelectorAll(node => node.localName === 'p' && node.textContent.startsWith('Current content comparison:'));
    assert.equal(comparisons.length,cold.rows.length);
    assert.ok(comparisons.some(node => node.textContent.includes(row.comparison)),'current comparison has its own full-panel display');
    assert.match(coldView.container.textContent,/Recorded lapse history/);
    assert.match(coldView.container.textContent,/lapsed \(subject absent\)/,'saved interval remains visible when current bytes match again');
  } finally {await coldView.close();}

  for (const [marker,expected,forbidden] of [
    ['FILE_ACT_LAPSE_PENDING_DTO:',/Save not established: 1/,/Observation saved: 1/],
    ['FILE_ACT_LAPSE_DISCLOSURE_PENDING_DTO:',/Observation saved: 1\. Late-write disclosure metadata is still pending/,/Save not established: 1/],
  ]) {
    const source = dto(marker);
    const held = source.lapseObservation.pending[0];
    const calls = [];
    const view = mounted(async (name,args) => {calls.push([name,args]);return source;});
    try {
      await view.show();
      assert.deepEqual(calls,[]);
      await view.press('Read file-act log and current content');
      assert.match(view.container.textContent,expected);
      assert.doesNotMatch(view.container.textContent,forbidden);
      assert.ok(view.container.textContent.includes(held.observedAt),'original observation time remains visible');
      await view.press('Retry saving held metadata only');
      assert.deepEqual(calls,[['file_act_read',{}],['file_act_retry_lapses',{}]],'renderer retries metadata without invoking capture or observing new content');
    } finally {await view.close();}
  }
});
