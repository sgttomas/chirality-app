// Mounted App: the Run a workflow guide's conversation actions select the
// run's own conversation and reveal it (its requests when Codex is waiting).
// Controlled invented host view; no supplier, model or person act.
import test from 'node:test';
import assert from 'node:assert/strict';
import {loadSrc} from './support/load-src.mjs';
import {installMiniDom} from './support/mini-dom.mjs';
import {installIdleNativeWaiting} from './support/idle-native-waiting.mjs';
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {App} = loadSrc('App');
const g = {home:'account', appSession:'s1', spawnCounter:1};
const key = id => JSON.stringify([g, id]);
const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const nodes = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const button = (c, label) => nodes(c, 'button').find(node => node.textContent === label);
const thread = id => ({generation:g, threadId:id, model:'invented-model', status:{type:'idle'}, appRole:{standing:'app-observed', role:null}, roleRelation:{kind:'start'}, futureGuidanceNotices:[]});
const open = {reference:'run-1', conversation:'T2', home:'account', source:'sent', workflow:{name:'invented-flow', origin:'project', revision:'r'}, lifecycle:{state:"open (live); only the person's explicit end ends it"}, status:{}};
const host = {state:'ready', generation:g, threads:[thread('T1'), thread('T2')], roleLimits:{account:{roles:[]}}, homeRouting:{activeModeHomeClass:'account'},
  serverRequests:[{recordKind:'server-request-entry', generation:g, requestIdentity:'q1', method:'item/tool/requestUserInput', classification:'known-answerable', originClass:'person-input',
    nativeParameters:{threadId:'T2', turnId:'t', itemId:'i', isBlocking:false, questions:[{id:'q', header:'Scope', question:'Which folder?', isOther:false, isSecret:false, options:[{label:'reports/', description:'Reports'}]}]},
    state:'outstanding', replyWriteResult:'not-attempted', acknowledgmentObservation:{status:'not-observed'}}],
  workflowRoot:{context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:null, libraries:[], selections:[], runs:[open], drafts:{drafts:[]}}};

test('Answer in the conversation selects the run conversation and reveals its requests, issuing no command', async () => {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c); const calls = [];
  const revealed = []; const previous = {getElementById:document.getElementById, setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval};
  document.getElementById = id => { revealed.push(id); return c.querySelectorAll(n => n.getAttribute('id') === id)[0] ?? null; };
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  const idle = installIdleNativeWaiting(async command => {
    calls.push(command);
    if (command === 'host_status') return structuredClone(host);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    assert.fail(`Unexpected IPC: ${command}`);
  });
  try {
    await React.act(async () => root.render(React.createElement(App)));
    const conversationSelect = () => nodes(c.querySelectorAll(n => n.getAttribute('id') === 'conversation')[0], 'select')[0];
    assert.equal(props(conversationSelect()).value, '', 'no operational conversation is chosen yet');
    const guideSelect = nodes(c, 'select').find(n => n.parentNode.textContent.startsWith('Conversation to run it in'));
    await React.act(async () => props(guideSelect).onChange({target:{value:'T2'}}));
    const before = calls.length;
    await React.act(async () => props(button(c, 'Answer in the conversation')).onClick());
    assert.equal(props(conversationSelect()).value, key('T2'), 'the run conversation is now the shown conversation');
    assert.ok(revealed.includes('conversation-requests'), 'its requests are revealed');
    assert.match(c.querySelectorAll(n => n.getAttribute('id') === 'conversation-requests')[0].textContent, /Which folder\?/);
    assert.deepEqual(calls.slice(before).filter(cmd => cmd !== 'host_status'), [], 'no answer, send or resume');
    idle.assertClean(c);
  } finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text); Object.assign(globalThis, {setInterval:previous.setInterval, clearInterval:previous.clearInterval}); document.getElementById = previous.getElementById; }
});

test('the ready trial link lands inside the clean trial composer, which says in plain words where it goes', async () => {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const previous = {getElementById:document.getElementById, setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval};
  document.getElementById = id => c.querySelectorAll(n => n.getAttribute('id') === id)[0] ?? null;
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  const {cleanTrialAnchor} = loadSrc('TrialComposer');
  const clean = {reference:'trial:clean-1', sequence:1, kind:'clean', draftName:'spacing-check', location:'project', card:'trial 1 of draft spacing-check', text:'[Chirality] Workflow trial 1', textIdentity:{value:'aa'}, bytes:28,
    message:'Inputs for this trial: …', authoring:null, cleanConversation:null, delegation:null, runInForce:null, draftChanged:null, workFolder:'.chirality/workflow-trials/w1', state:'pre-filled', limit:null};
  const withTrial = {...host, workflowRoot:{...host.workflowRoot, pendingTrials:[clean]}};
  const calls = [];
  const idle = installIdleNativeWaiting(async command => {
    calls.push(command);
    if (command === 'host_status') return structuredClone(withTrial);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    assert.fail(`Unexpected IPC: ${command}`);
  });
  try {
    await React.act(async () => root.render(React.createElement(App)));
    const anchor = cleanTrialAnchor('trial:clean-1');
    const panel = c.querySelectorAll(n => n.getAttribute('id') === anchor)[0];
    assert.ok(panel, 'the clean composer has its own place');
    assert.equal(panel.getAttribute('aria-label'), 'New trial conversation');
    const owner = c.querySelectorAll(n => n.getAttribute('aria-label') === 'Original composer owner')[0].textContent;
    assert.match(owner, /^This trial starts its own new conversation; it isn't sent in an existing one\./);
    assert.match(owner, /Exact scopeTrial reference trial:clean-1\./, 'the exact scope stays under details');
    assert.doesNotMatch(c.textContent, /global clean composer|render owner/);
    const main = c.querySelectorAll(n => n.localName === 'main')[0];
    const link = document.createElement('a'); link.setAttribute('href', `#${anchor}`); main.appendChild(link);
    let prevented = false;
    await React.act(async () => props(main).onClick({target:link, currentTarget:main, preventDefault:() => { prevented = true; }}));
    assert.equal(prevented, true);
    const active = nodes(c, 'a').filter(a => a.getAttribute('aria-current') === 'page').map(a => a.textContent);
    assert.deepEqual(active, ['Conversation'], 'the Conversation view is shown');
    assert.equal(panel.getAttribute('tabindex'), '-1', 'focus lands on the composer itself, not the conversation select above it');
    main.removeChild(link);
    assert.deepEqual(calls.filter(cmd => !['host_status', 'decision_view', 'native_confirmation_content'].includes(cmd)), [], 'following the link issues no action');
  } finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text); Object.assign(globalThis, {setInterval:previous.setInterval, clearInterval:previous.clearInterval}); document.getElementById = previous.getElementById; }
});
