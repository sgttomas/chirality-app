import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, readFileSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawnSync} from 'node:child_process';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// The maintained actual Host/role/HomeRouter journey produces these packets.
// No invented renderer acceptance flag or error string classifies the sender.
// A checked producer directory may be reused for UI-only integration checks.
// Ordinary runs still execute the maintained native producer in fresh scratch.
const retainedFixture = process.env.CHIRALITY_CONTINUE_AS_FIXTURE_DIR;
const fixture = retainedFixture ?? mkdtempSync(join(tmpdir(), 'chirality-handoff-native-'));
if (!retainedFixture) {
  const native = spawnSync('cargo', ['test','--offline','--locked','--lib','producer_receipts_preserve_native_ack_refusal_error_unknown_and_late_response','--','--nocapture'], {
    cwd:fileURLToPath(new URL('../src-tauri',import.meta.url)), encoding:'utf8', timeout:180000,
    env:{...process.env, CHIRALITY_SKIP_CODEX:'1', CARGO_NET_OFFLINE:'true', CHIRALITY_HANDOFF_FIXTURE_DIR:fixture, TMPDIR:fixture},
  });
  writeFileSync(join(fixture,'producer.log'),`${native.stdout ?? ''}${native.stderr ?? ''}`);
  assert.equal(native.status,0,`native producer fixture failed: ${native.error ?? native.stderr}\n${native.stdout}`);
}
assert.match(readFileSync(join(fixture,'producer.log'),'utf8'),/test result: ok\. [1-9]\d* passed; 0 failed;/,'packets accompany a successful actual producer run');
const packet = name => JSON.parse(readFileSync(join(fixture,`${name}.json`),'utf8'));
const sent = packet('sent'), refused = packet('not-attempted'), failed = packet('native-failed'), unknown = packet('unknown'), late = packet('late-sent');
console.log(`Continue-as actual producer packets: ${fixture}`);
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App} = loadSrc('App');
const props = element => element[Object.keys(element).find(key => key.startsWith('__reactProps$'))];
const elements = (container,tag) => container.querySelectorAll(element => element.localName === tag);
const button = (container,label) => elements(container,'button').find(element=>element.textContent===label);
const sendLabel = 'Send this message to the new conversation';
const readLabel = 'Read the original send outcome';

async function mounted(basis, command, run, {refreshFails=false, observeStatus}={}) {
  const container=document.createElement('div');document.body.appendChild(container);
  const root=createRoot(container), calls=[], unexpected=[];
  let afterSend=false;
  const before=structuredClone(basis.snapshot), snapshot=structuredClone(basis.snapshot);
  const idle=installIdleNativeWaiting(async(name,args)=>{
    calls.push({name,args});
    if(name==='host_status') {if(afterSend&&refreshFails)throw Error('synthetic observer refresh unavailable');if(observeStatus)await observeStatus(afterSend);return snapshot;}
    if(name==='decision_view')return {rows:[]};
    if(name==='native_confirmation_content')return [];
    if(name==='host_observe') {
      assert.deepEqual(args,{sourceGeneration:basis.generation,generation:null,after:0});
      return basis.windowObservation; // actual read-only attachment, no supplier action
    }
    if(name==='continue_as_send') {
      afterSend=true;
      assert.deepEqual(Object.keys(args).sort(),['id','text'],'renderer supplies no home/generation/thread/role authority');
      assert.equal(args.id,basis.handoffId);
      return command(name,args,calls.filter(call=>call.name==='continue_as_send').length);
    }
    if(name==='continue_as_send_read') {
      assert.deepEqual(args,{id:basis.handoffId},'read selects the retained original handoff only');
      return command(name,args);
    }
    unexpected.push({name,args});throw Error(`Unexpected original command: ${name}`);
  });
  const panel=()=>container.querySelectorAll(e=>e.getAttribute('aria-label')==='Continue as')[0];
  const press=async label=>React.act(async()=>{const b=button(panel(),label);assert.ok(b,label);assert.equal(props(b).disabled,false,label);props(b).onClick();});
  const change=async text=>React.act(()=>props(elements(panel(),'textarea')[0]).onChange({target:{value:text}}));
  try {
    await React.act(async()=>root.render(React.createElement(App)));
    assert.ok(panel(),'actual App mounts actual ContinueAsPanel');
    assert.equal(calls.filter(call=>call.name==='continue_as_send').length,0,'mount sends nothing');
    if(props(elements(panel(),'textarea')[0]).disabled) assert.equal(props(elements(panel(),'textarea')[0]).value,basis.editedText);
    else await change(basis.editedText);
    assert.equal(calls.filter(call=>call.name==='continue_as_send').length,0,'editing sends nothing');
    await run({container,panel,press,change,calls,send:()=>button(panel(),sendLabel),draft:()=>props(elements(panel(),'textarea')[0]).value});
    assert.deepEqual(unexpected,[],'strict original dispatcher saw no implicit command');
    assert.deepEqual(snapshot,before,'the mounted consumer cannot replace a native target, role or source');
    idle.assertClean(container);
  } finally {
    const renderedText=container.textContent;
    try {await React.act(()=>root.unmount());}
    finally {document.body.removeChild(container);idle.restore(renderedText);}
  }
}

for(const refreshFails of [false,true])test(`actual native receipt remains sent when observer refresh ${refreshFails?'fails':'succeeds'}`,async()=>{
  await mounted(sent,async(_name,args)=>{assert.equal(args.text,sent.editedText);return sent.outcome;},async ui=>{
    await ui.press(sendLabel);
    assert.match(ui.panel().textContent,/Sent once as an ordinary message/);
    assert.doesNotMatch(ui.panel().textContent,/Not sent:|You can send it again|Nothing has been sent to it/);
    assert.equal(props(ui.send()).disabled,true);
    assert.equal(ui.draft(),sent.editedText);
    assert.equal(ui.calls.filter(c=>c.name==='continue_as_send').length,1);
    if(refreshFails)assert.match(ui.panel().textContent,/View refresh unavailable: Error: synthetic observer refresh unavailable/);
  },{refreshFails});
});

test('actual proved pre-write refusal retains editable text and allows one explicit retry',async()=>{
  assert.equal(refused.handoffId,sent.handoffId);
  await mounted(refused,async(_name,args,index)=>{assert.equal(args.text,refused.editedText);return index===1?refused.outcome:sent.outcome;},async ui=>{
    await ui.press(sendLabel);assert.match(ui.panel().textContent,/native owner established that no write attempt occurred/);
    assert.equal(props(ui.send()).disabled,false);assert.equal(ui.draft(),refused.editedText);
    assert.equal(ui.calls.filter(c=>c.name==='continue_as_send').length,1,'no retry without another press');
    await ui.press(sendLabel);assert.match(ui.panel().textContent,/Sent once/);
    assert.equal(ui.calls.filter(c=>c.name==='continue_as_send').length,2);
  });
});

test('actual native error remains distinct from not-attempted and unknown',async()=>{
  await mounted(failed,async()=>failed.outcome,async ui=>{
    await ui.press(sendLabel);assert.match(ui.panel().textContent,/original request received a native error: synthetic handoff native refusal/);
    assert.doesNotMatch(ui.panel().textContent,/Not sent:|Sent once|Send outcome unknown/);
    assert.equal(props(ui.send()).disabled,true);assert.equal(ui.draft(),failed.editedText);
  });
});

test('actual pending source stays unknown, and a person-directed read joins its late response without resend',async()=>{
  assert.equal(unknown.outcome.attemptRef,late.outcome.attemptRef);
  await mounted(unknown,async name=>name==='continue_as_send'?unknown.outcome:late.outcome,async ui=>{
    await ui.press(sendLabel);assert.match(ui.panel().textContent,/Send outcome unknown/);
    assert.doesNotMatch(ui.panel().textContent,/Not sent:|not accepted|You can send it again/);
    assert.equal(props(ui.send()).disabled,true);assert.equal(ui.draft(),unknown.editedText);
    await ui.press(readLabel);assert.match(ui.panel().textContent,/Sent once/);
    assert.equal(ui.calls.filter(c=>c.name==='continue_as_send').length,1);
    assert.equal(ui.calls.filter(c=>c.name==='continue_as_send_read').length,1);
  });
});

test('remounting an observed unknown handoff retains its exact original edited draft and sends nothing',async()=>{
  assert.equal(unknown.observedSnapshot.continueAs[0].draftText,unknown.editedText);
  await mounted({...unknown,snapshot:unknown.observedSnapshot},async()=>{throw Error('remount must not dispatch');},async ui=>{
    assert.match(ui.panel().textContent,/Send outcome unknown/);
    assert.equal(ui.draft(),unknown.editedText);
    assert.equal(props(ui.send()).disabled,true);
    assert.equal(ui.calls.filter(c=>c.name==='continue_as_send').length,0);
  });
});

test('queued duplicate presses and an unconfirmed IPC/read failure never offer proved-unsent retry',async()=>{
  let release;const held=new Promise(resolve=>{release=resolve;});
  await mounted(sent,async name=>{if(name==='continue_as_send'){await held;throw Error('IPC result unavailable');}throw Error('original read unavailable');},async ui=>{
    const click=props(ui.send()).onClick;
    await React.act(()=>{click();click();});
    assert.equal(ui.calls.filter(c=>c.name==='continue_as_send').length,1,'same-render duplicate is latched');
    assert.equal(props(ui.send()).disabled,true);
    await React.act(async()=>{release();});
    assert.match(ui.panel().textContent,/Send outcome unknown: Error: IPC result unavailable/);
    await ui.press(readLabel);assert.match(ui.panel().textContent,/Send outcome unknown/);
    assert.equal(props(ui.send()).disabled,true);assert.equal(ui.draft(),sent.editedText);
    assert.equal(ui.calls.filter(c=>c.name==='continue_as_send').length,1);
  });
});

test('a delayed first observer completion cannot expose its old no-attempt result against a newer explicit send',async()=>{
  let releaseOldObserver,releaseSecondSend;
  const oldObserver=new Promise(resolve=>{releaseOldObserver=resolve;});
  const secondSend=new Promise(resolve=>{releaseSecondSend=resolve;});
  let holdFirst=true;
  await mounted(refused,async(name,_args,index)=>{
    if(name==='continue_as_send_read')return refused.outcome;
    if(index===1)return refused.outcome;
    await secondSend;return sent.outcome;
  },async ui=>{
    await ui.press(sendLabel);assert.match(ui.panel().textContent,/Waiting for the original send/);
    await ui.press(readLabel);assert.match(ui.panel().textContent,/no write attempt occurred/);
    assert.equal(props(ui.send()).disabled,false);
    await ui.press(sendLabel);assert.equal(props(ui.send()).disabled,true);
    await React.act(async()=>{releaseOldObserver();});
    assert.match(ui.panel().textContent,/Waiting for the original send/);
    assert.doesNotMatch(ui.panel().textContent,/Not sent:|you can send it again/);
    assert.equal(props(ui.send()).disabled,true,'the old no-attempt cannot release the new attempt latch');
    assert.equal(ui.calls.filter(c=>c.name==='continue_as_send').length,2);
    await React.act(async()=>{releaseSecondSend();});assert.match(ui.panel().textContent,/Sent once/);
  },{observeStatus:async afterSend=>{if(afterSend&&holdFirst){holdFirst=false;await oldObserver;}}});
});
