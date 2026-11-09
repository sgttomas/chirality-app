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
const open = {reference:'run-1', conversation:'T2', home:'account', generation:g, source:'sent', workflow:{name:'invented-flow', origin:'project', revision:'r'}, lifecycle:{state:"open (live); only the person's explicit end ends it"}, status:{}};
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

test('a run\'s "recorded evidence" link lands on that run in the workflow studio', async () => {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const previous = {getElementById:document.getElementById, setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval};
  document.getElementById = id => c.querySelectorAll(n => n.getAttribute('id') === id)[0] ?? null;
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  const {runEvidenceAnchor} = loadSrc('RunJourney');
  const idle = installIdleNativeWaiting(async command => {
    if (command === 'host_status') return structuredClone(host);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    assert.fail(`Unexpected IPC: ${command}`);
  });
  try {
    await React.act(async () => root.render(React.createElement(App)));
    const anchor = runEvidenceAnchor('run-1');
    const article = c.querySelectorAll(n => n.getAttribute('id') === anchor)[0];
    assert.ok(article, 'the studio\'s run article has its own place');
    assert.match(article.textContent, /run-1/);
    const main = c.querySelectorAll(n => n.localName === 'main')[0];
    const link = document.createElement('a'); link.setAttribute('href', `#${anchor}`); main.appendChild(link);
    let prevented = false;
    await React.act(async () => props(main).onClick({target:link, currentTarget:main, preventDefault:() => { prevented = true; }}));
    assert.equal(prevented, true);
    assert.equal(article.getAttribute('tabindex'), '-1', 'focus lands on that run');
    const view = article; let owner = null;
    for (let node = view; node; node = node.parentNode) { const v = node.getAttribute?.('data-workspace-view'); if (v) { owner = node; break; } }
    assert.ok(owner && !owner.hidden, 'its view is shown');
    main.removeChild(link);
  } finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text); Object.assign(globalThis, {setInterval:previous.setInterval, clearInterval:previous.clearInterval}); document.getElementById = previous.getElementById; }
});

test('a saved trial conversation opens History with only its ID in the search: nothing is read, chosen or continued', async () => {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const previous = {getElementById:document.getElementById, setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval};
  document.getElementById = id => c.querySelectorAll(n => n.getAttribute('id') === id)[0] ?? null;
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  const cold = {reference:'trial:lib:1', sequence:1, kind:'clean', content:{value:'c'}, version:'current', trialConversation:'thread-old-trial', authoringConversation:'thread-old-authoring',
    authoringSourceLimit:'Original authoring source is not established by this saved trial link; choose a current target', sourceLimit:'Original trial source is not established by this saved trial link; no native history read', broughtBack:[], time:'t', link:{}, standing:'s', fidelity:{}};
  const withDraft = {...host, workflowRoot:{...host.workflowRoot, activeLibrary:'lib:project', libraries:[{reference:'lib:project', origin:'project', root:{encoding:'unix_bytes', bytes:[...new TextEncoder().encode('/invented/project')]}, registered:[]}],
    drafts:{drafts:[{name:'spacing-check', state:'draft', trials:[cold]}]}}};
  const calls = [];
  const idle = installIdleNativeWaiting(async command => {
    calls.push(command);
    if (command === 'host_status') return structuredClone(withDraft);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    assert.fail(`Unexpected IPC: ${command}`);
  });
  try {
    await React.act(async () => root.render(React.createElement(App)));
    const guide = c.querySelectorAll(n => n.getAttribute('aria-label') === 'Make a workflow from your work')[0];
    await React.act(async () => props(nodes(guide, 'input')[0]).onChange({target:{value:'spacing-check'}}));
    const look = nodes(guide, 'button').find(n => n.textContent === 'Look for it in History');
    assert.ok(look);
    await React.act(async () => props(look).onClick());
    const active = c.querySelectorAll(n => n.localName === 'a' && n.getAttribute('aria-current') === 'page').map(n => n.textContent);
    assert.deepEqual(active, ['History'], 'History is shown');
    const search = c.querySelectorAll(n => n.localName === 'input' && n.getAttribute('aria-describedby') === 'history-search-count')[0];
    assert.equal(props(search).value, 'thread-old-trial', 'its search holds the saved ID');
    assert.match(c.querySelectorAll(n => n.getAttribute('aria-label') === 'Searching for a saved conversation')[0].textContent, /It is only a search: nothing is read, chosen or continued\. If it isn't among the received conversations, it may be in another home/);
    assert.deepEqual(calls.filter(cmd => !['host_status', 'decision_view', 'native_confirmation_content'].includes(cmd)), [], 'no history read, selection, home change or Continue');
  } finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text); Object.assign(globalThis, {setInterval:previous.setInterval, clearInterval:previous.clearInterval}); document.getElementById = previous.getElementById; }
});

test('a registered revision to re-confirm links from Run to its own row in the workflow studio, issuing no command', async () => {
  const c = document.createElement('div'); document.body.appendChild(c); const root = createRoot(c);
  const previous = {getElementById:document.getElementById, setInterval:globalThis.setInterval, clearInterval:globalThis.clearInterval};
  document.getElementById = id => c.querySelectorAll(n => n.getAttribute('id') === id)[0] ?? null;
  globalThis.setInterval = () => 0; globalThis.clearInterval = () => {};
  const {registeredRevisionAnchor} = loadSrc('RunJourney');
  const cold = {name:'load-check', sequence:1, revision:'b'.repeat(64), label:'registered — re-confirm to use in this App session', selectable:false, reconfirm:true, offered:'Refine (RF-1); Review a draft with its bytes (DS-8)'};
  const library = {reference:'lib-1', origin:'project', root:'/p/.chirality', sourceRoot:'src', registered:[cold], entryListing:{state:'not observed', entries:[], limits:[]}};
  const withLibrary = {...host, workflowRoot:{...host.workflowRoot, activeLibrary:'lib-1', libraries:[library]}};
  const calls = [];
  const idle = installIdleNativeWaiting(async command => {
    calls.push(command);
    if (command === 'host_status') return structuredClone(withLibrary);
    if (command === 'decision_view') return {rows:[]};
    if (command === 'native_confirmation_content') return [];
    assert.fail(`Unexpected IPC: ${command}`);
  });
  try {
    await React.act(async () => root.render(React.createElement(App)));
    const anchor = registeredRevisionAnchor('lib-1', 'load-check', 'b'.repeat(64));
    assert.notEqual(anchor, registeredRevisionAnchor('lib-1', 'load-check', 'a'.repeat(64)), 'each revision has its own place');
    const row = c.querySelectorAll(n => n.getAttribute('id') === anchor)[0];
    assert.ok(row, 'the studio row has its own place');
    assert.match(row.textContent, /re-confirmation/);
    assert.ok(nodes(row, 'button').some(b => b.textContent === 'Refine from the revision store…'));
    const link = nodes(c, 'a').find(a => a.textContent === 'Re-confirm load-check in the workflow studio');
    assert.ok(link, 'the Run guide offers the re-confirmation route');
    assert.equal(link.getAttribute('href'), `#${anchor}`);
    const main = nodes(c, 'main')[0];
    let prevented = false;
    await React.act(async () => props(main).onClick({target:link, currentTarget:main, preventDefault:() => { prevented = true; }}));
    assert.equal(prevented, true);
    assert.equal(row.getAttribute('tabindex'), '-1', 'focus lands on that revision');
    let owner = null;
    for (let node = row; node; node = node.parentNode) { const v = node.getAttribute?.('data-workspace-view'); if (v) { owner = node; break; } }
    assert.ok(owner && !owner.hidden, 'its view is shown');
    assert.deepEqual(calls.filter(cmd => !['host_status', 'decision_view', 'native_confirmation_content'].includes(cmd)), [], 'following the link refines, reviews and selects nothing');
  } finally { const text = c.textContent; await React.act(() => root.unmount()); document.body.removeChild(c); idle.restore(text); Object.assign(globalThis, {setInterval:previous.setInterval, clearInterval:previous.clearInterval}); document.getElementById = previous.getElementById; }
});
