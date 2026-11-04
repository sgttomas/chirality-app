import test from 'node:test';
import assert from 'node:assert/strict';
import {installMiniDom} from './support/mini-dom.mjs';
import {loadSrc} from './support/load-src.mjs';

// J2 guided path: the App composes a draft request for the person to send;
// finding, trial, review and registration stay on existing host commands.
// Controlled host views only: no native App, supplier, model or person act.
const document = installMiniDom();
const React = (await import('react')).default;
const {createRoot} = await import('react-dom/client');
const {MakeWorkflowGuide, validWorkflowName, draftFolder, draftRequestText} = loadSrc('MakeJourney');
const {ConversationPanel} = loadSrc('App');

const g = {home:'account', appSession:'s1', spawnCounter:1};
const path = text => ({encoding:'unix_bytes', bytes:[...new TextEncoder().encode(text)]});
const key = threadId => JSON.stringify([g, threadId]);
const host = (over = {}) => ({state:'ready', generation:g, workflowRoot:{context:{sourceRef:'src', generation:g}},
  threads:[{threadId:'T1', generation:g, model:'invented-model'}, {threadId:'T2', generation:g, model:'invented-model'}], ...over});
const data = (over = {}) => ({context:{sourceRef:'src', generation:g}, projectLibraryAvailable:true, activeLibrary:'lib:project',
  libraries:[{reference:'lib:project', origin:'project', root:path('/invented/project'), registered:[{name:'taken-name', sequence:1, revision:'r', selectable:true}]}],
  drafts:{drafts:[]}, ...over});

const props = node => node[Object.keys(node).find(k => k.startsWith('__reactProps$'))];
const all = (c, tag) => c.querySelectorAll(node => node.localName === tag);
const button = (c, label) => all(c, 'button').find(node => node.textContent === label);
const region = (c, label) => c.querySelectorAll(node => node.getAttribute('aria-label') === label)[0];
const next = c => region(c, 'Make a workflow from your work').textContent.match(/Next: ([^]*?)(?=Where you did the work)/)?.[1] ?? '';

async function mount(view) {
  const c = document.createElement('div'); const root = createRoot(c); const calls = []; const offers = [];
  const opened = [];
  const render = () => root.render(React.createElement(MakeWorkflowGuide, {data:view.data, host:view.host, busy:!!view.busy, uncertainBringBacks:view.uncertain ?? [], acknowledgeBringBack:trial => (view.acknowledged ??= []).push(trial),
    act:async (command, args) => { calls.push({command, args}); }, offerComposer:(threadKey, text) => offers.push({threadKey, text}), openPreparedMessage:item => opened.push(item),
    showConversation:view.navigate ? id => opened.push({shown:id}) : undefined}));
  await React.act(async () => render());
  return {c, calls, offers, opened, rerender:async next => { Object.assign(view, next); await React.act(async () => render()); },
    choose:async value => React.act(async () => props(all(c, 'select')[0]).onChange({target:{value}})),
    name:async value => React.act(async () => props(all(c, 'input')[0]).onChange({target:{value}})),
    press:async label => { const node = button(c, label); assert.ok(node, label); assert.equal(!!props(node).disabled, false, `${label} enabled`); await React.act(async () => props(node).onClick()); }};
}

test('the name rule and draft folder follow the host', () => {
  for (const name of ['spacing-check', 'a', 'v2-report', 'x'.repeat(64)]) assert.equal(validWorkflowName(name), true, name);
  for (const name of ['', 'Spacing', 'two--hyphens', '-lead', 'trail-', 'with space', 'under_score', 'x'.repeat(65)]) assert.equal(validWorkflowName(name), false, name);
  assert.equal(draftFolder('/invented/project/', 'spacing-check'), '/invented/project/.chirality/workflow-drafts/spacing-check');
  const request = draftRequestText('/invented/project/.chirality/workflow-drafts/spacing-check', 'spacing-check');
  assert.match(request, /\/invented\/project\/\.chirality\/workflow-drafts\/spacing-check\/WORKFLOW\.md starts with front matter holding only `name: spacing-check`/);
  assert.match(request, /Only write inside that folder\. Don't register it/);
});

test('a request is composed for the chosen conversation only once each prerequisite is met, and nothing is sent', async () => {
  const ui = await mount({host:host(), data:data()});
  assert.match(next(ui.c), /Choose the conversation where you did the work/);
  await ui.choose(key('T1'));
  assert.match(next(ui.c), /Name the workflow/);
  await ui.name('Bad Name'); assert.match(next(ui.c), /lowercase letters and digits only/);
  await ui.name('taken-name'); assert.match(next(ui.c), /already registered in this library; a new draft with that name would be refused/);
  assert.equal(props(button(ui.c, 'Put the request in the conversation')).disabled, true);
  await ui.name('spacing-check');
  assert.match(region(ui.c, 'Make a workflow from your work').textContent, /It will be written to \/invented\/project\/\.chirality\/workflow-drafts\/spacing-check\./);
  await ui.press('Put the request in the conversation');
  assert.deepEqual(ui.offers, [{threadKey:key('T1'), text:draftRequestText('/invented/project/.chirality/workflow-drafts/spacing-check', 'spacing-check')}]);
  assert.deepEqual(ui.calls, [], 'composing the request issues no host command');
  await ui.press('Look for drafts in this library');
  assert.deepEqual(ui.calls, [{command:'workflow_observe_drafts', args:{}}]);
  assert.match(region(ui.c, 'Make a workflow from your work').textContent, /No draft named spacing-check has been seen yet/);
});

test('each draft state names its own next step; registration is never claimed before the host reports it', async () => {
  const ui = await mount({host:host(), data:data()});
  await ui.choose(key('T1')); await ui.name('spacing-check');
  const cases = [
    [{state:'not valid', findings:['HY-2: front-matter name "x" differs from the folder name "spacing-check"']}, /not valid for registration.*HY-2.*Ask the agent to fix the findings/, '#conversation'],
    [{state:'draft'}, /draft — not registered.*Only your confirmation registers it/, '#workflow-drafts'],
    [{state:'under review', content:{value:'abcdef0123456789'}}, /under review.*A review was started, but its confirmation isn't available here now/, '#workflow-reviews'],
    [{state:'changed since review'}, /changed since review.*Review again before registering/, '#workflow-drafts'],
    [{state:'registered, unchanged since'}, /registered, unchanged since.*use it from Run a workflow/, '#run-workflow'],
  ];
  for (const [draft, words, href] of cases) {
    await ui.rerender({data:data({drafts:{drafts:[{name:'spacing-check', ...draft}]}})});
    const status = region(ui.c, 'Draft status');
    assert.match(status.textContent, words, draft.state); assert.ok(all(status, 'a').some(a => a.getAttribute('href') === href), `${draft.state} → ${href}`);
    if (draft.state !== 'registered, unchanged since') assert.doesNotMatch(status.textContent, /Registered\. You can now use it/, draft.state);
    const step = next(ui.c).trim();
    assert.ok(step.startsWith('spacing-check: '), `the top Next names the draft's own step (${draft.state})`);
    assert.ok(status.textContent.includes(step.slice('spacing-check: '.length)), `the top Next is the draft's current step, not a stale one (${draft.state})`);
    assert.equal(props(button(ui.c, 'Put the request in the conversation')).disabled, true, 'an existing draft is continued, not requested again');
  }
});

test('unfinished drafts are listed for return after reopening and Continue only fills the local name', async () => {
  const drafts = [{name:'half-done', state:'draft'}, {name:'needs-fix', state:'not valid', findings:['HY-1: no WORKFLOW.md']}, {name:'finished-one', state:'registered, unchanged since'}, {name:'gone', state:'removed'}];
  const ui = await mount({host:host(), data:data({drafts:{drafts}})});
  const list = region(ui.c, 'Unfinished drafts').textContent;
  assert.match(list, /half-done/); assert.match(list, /needs-fix/); assert.doesNotMatch(list, /finished-one|gone/);
  assert.match(list, /still here after you quit and reopen the App.*reading one there doesn't continue it/);
  await ui.press('Continue needs-fix');
  assert.equal(props(all(ui.c, 'input')[0]).value, 'needs-fix');
  assert.match(region(ui.c, 'Draft status').textContent, /HY-1: no WORKFLOW\.md/);
  assert.deepEqual(ui.calls, []); assert.deepEqual(ui.offers, []);
});

test('no library, stale source and busy states issue nothing', async () => {
  const ui = await mount({host:host(), data:data({activeLibrary:null})});
  await ui.choose(key('T1')); await ui.name('spacing-check');
  assert.match(next(ui.c), /Show this project's workflows so the draft has a place to go/);
  await ui.press('Show this project\'s workflows');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_open_project_library', args:{}});
  ui.calls.length = 0;
  await ui.rerender({host:host({workflowRoot:{context:{sourceRef:'other', generation:g}}}), data:data()});
  assert.match(next(ui.c), /out of date/);
  for (const label of ['Put the request in the conversation', 'Look for drafts in this library']) {
    const node = button(ui.c, label); assert.equal(props(node).disabled, true, label); await React.act(async () => props(node).onClick());
  }
  assert.equal(props(all(ui.c, 'select')[0]).disabled, true);
  assert.deepEqual(ui.calls, []); assert.deepEqual(ui.offers, []);
});

test('an offered request fills only an empty composer of its conversation, keeps unsent text, and is never sent', async () => {
  const container = document.createElement('div'); document.body.appendChild(container); const root = createRoot(container);
  const sends = []; const noop = async () => {};
  const panelHost = {state:'ready', generation:g, roleLimits:{account:{roles:[]}}, threads:[{generation:g, threadId:'T1', futureGuidanceNotices:[]}, {generation:g, threadId:'T2', futureGuidanceNotices:[]}]};
  const show = (threadKey, composerOffer) => React.act(async () => root.render(React.createElement(ConversationPanel, {host:panelHost, threadKey, composerOffer, setThreadKey:() => {},
    answer:noop, runAct:noop, send:async (...args) => { sends.push(args); }, steer:noop, submitAttachments:noop, interrupt:noop, checkPlanMode:noop, codexBusy:false})));
  const textarea = () => all(container, 'textarea').find(node => node.parentNode.textContent.startsWith('Text '));
  const revealed = [];
  document.getElementById = id => { revealed.push(id); return container.querySelectorAll(node => node.getAttribute('id') === id)[0] ?? null; };
  await show(key('T1'), null);
  await show(key('T1'), {sequence:1, threadKey:key('T2'), text:'for T2'});
  assert.equal(props(textarea()).value, '', 'another conversation\'s request waits for that conversation');
  await show(key('T1'), {sequence:2, threadKey:key('T1'), text:'Please write the draft'});
  assert.equal(props(textarea()).value, 'Please write the draft');
  await React.act(async () => props(textarea()).onChange({target:{value:'my own unsent words'}}));
  await show(key('T1'), {sequence:3, threadKey:key('T1'), text:'A newer request'});
  assert.equal(props(textarea()).value, 'my own unsent words', 'unsent text is never replaced by an offer');
  assert.match(region(container, 'Prepared workflow request').textContent, /Your unsent text is kept/);
  await show(key('T1'), {sequence:3, threadKey:key('T1'), text:'A newer request'});
  await React.act(async () => props(button(container, 'Replace my text with the request')).onClick());
  assert.equal(props(textarea()).value, 'A newer request');
  assert.equal(region(container, 'Prepared workflow request'), undefined);
  await show(key('T1'), {sequence:3, threadKey:key('T1'), text:'A newer request'});
  await React.act(async () => props(textarea()).onChange({target:{value:''}}));
  await show(key('T1'), {sequence:3, threadKey:key('T1'), text:'A newer request'});
  assert.equal(props(textarea()).value, '', 'a handled offer is applied once');
  assert.deepEqual(sends, [], 'nothing is sent by an offer');
  assert.deepEqual(revealed, ['conversation', 'conversation'], 'each applied or held offer reveals the conversation once');
  await React.act(async () => root.unmount());
});

test('after reopening, the library comes first so unfinished drafts appear before any conversation is chosen', async () => {
  const ui = await mount({host:host(), data:data({activeLibrary:null})});
  assert.match(next(ui.c), /Show this project's workflows so the draft has a place to go, and to see unfinished drafts/);
  await ui.press('Show this project\'s workflows');
  await ui.rerender({data:data({drafts:{drafts:[{name:'half-done', state:'draft'}]}})});
  assert.match(region(ui.c, 'Unfinished drafts').textContent, /half-done/);
  assert.match(next(ui.c), /Choose the conversation where you did the work/);
});

test('a listed draft is tried and reviewed with the draft list\'s own commands and the guide\'s conversation', async () => {
  const ui = await mount({host:host(), data:data({drafts:{drafts:[{name:'spacing-check', state:'draft'}]}})});
  await ui.name('spacing-check');
  assert.equal(props(button(ui.c, 'Try it with the agent in this conversation')).disabled, true, 'a delegated trial needs the conversation');
  await ui.choose(key('T1'));
  await ui.press('Try it with the agent in this conversation');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_trial_prepare', args:{name:'spacing-check', kind:'delegated', generation:g, threadId:'T1'}});
  await ui.press('Try it in a fresh conversation');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_trial_prepare', args:{name:'spacing-check', kind:'clean', generation:g, threadId:'T1'}});
  await ui.press('Review it for registration…');
  assert.deepEqual(ui.calls.at(-1), {command:'workflow_review_draft', args:{name:'spacing-check'}});
  assert.match(region(ui.c, 'Try or review this draft').textContent, /only your confirmation in the App's dialog registers it/);
  const delegated = {draftName:'spacing-check', sequence:1, reference:'p1', authoring:{generation:g, threadId:'T1'}};
  await ui.rerender({host:host({threads:[{threadId:'T1', generation:g, model:'m', delegation:{reading:'missing', reason:'invented: no sub-agent tool'}}, {threadId:'T2', generation:g, model:'m'}]}),
    data:data({drafts:{drafts:[{name:'spacing-check', state:'changed since review', tryLimit:'invented try limit', reviewLimit:'invented review limit'}]}})});
  const actions = region(ui.c, 'Try or review this draft');
  assert.equal(button(ui.c, 'Try it with the agent in this conversation'), undefined, 'missing delegation hides the delegated trial');
  assert.match(actions.textContent, /isn't available in this conversation: invented: no sub-agent tool/);
  for (const label of ['Try it in a fresh conversation', 'Review it for registration…']) assert.equal(props(button(ui.c, label)).disabled, true, label);
  assert.match(actions.textContent, /invented try limit.*invented review limit/);
  await ui.rerender({data:data({drafts:{drafts:[{name:'spacing-check', state:'under review'}]}})});
  assert.equal(region(ui.c, 'Try or review this draft'), undefined, 'an open review is continued in the review, not reopened here');
  await ui.rerender({data:data({drafts:{drafts:[{name:'spacing-check', state:'not valid', findings:['HY-1: no WORKFLOW.md']}]}})});
  assert.equal(region(ui.c, 'Try or review this draft'), undefined, 'an invalid draft is fixed first');
  const withPending = host({homeRouting:{activeModeHomeClass:'account'}, workflowRoot:{context:{sourceRef:'src', generation:g},
    pendingTrials:[{kind:'delegated', ...delegated}, {kind:'clean', draftName:'spacing-check', sequence:2, reference:'p2'}, {kind:'delegated', draftName:'other-draft', sequence:3, reference:'p3', authoring:{generation:g, threadId:'T1'}}]}});
  await ui.rerender({host:withPending, data:data({drafts:{drafts:[{name:'spacing-check', state:'draft'}]}})});
  const ready = region(ui.c, 'Try or review this draft').textContent;
  assert.match(ready, /Trial 1 is ready to send/); assert.match(ready, /Trial 2 is ready to send\. Read and send it in the new-trial message box/);
  const {cleanTrialAnchor} = loadSrc('TrialComposer');
  assert.equal(region(ui.c, 'Try or review this draft').querySelectorAll(n => n.localName === 'a').find(a => a.textContent === 'Read and send it in the new-trial message box').getAttribute('href'), `#${cleanTrialAnchor('p2')}`, 'the link goes to that trial\'s own composer');
  assert.doesNotMatch(ready, /Trial 3/, 'another draft\'s trial is not offered here');
  const before = ui.calls.length;
  await ui.press('Read and send trial 1');
  assert.equal(ui.opened.length, 1); assert.equal(ui.opened[0].kind, 'delegated'); assert.equal(ui.opened[0].pending.reference, 'p1');
  assert.equal(ui.calls.length, before, 'opening a prepared trial issues no command and sends nothing');
});

test('with App navigation, an invalid draft shows its conversation instead of a bare scroll link', async () => {
  const ui = await mount({navigate:true, host:host(), data:data({drafts:{drafts:[{name:'spacing-check', state:'not valid', findings:['HY-1: no WORKFLOW.md']}]}})});
  await ui.choose(key('T1')); await ui.name('spacing-check');
  await ui.press('Show the conversation');
  assert.deepEqual(ui.opened, [{shown:'T1'}]);
  assert.deepEqual(ui.calls, []); assert.deepEqual(ui.offers, []);
});

// Rows as the host lists them: workflow_trials.rs trials_for_draft (newest
// first; clean `trialConversation` and `broughtBack[].to` are saved bare IDs)
// and trial_flows.rs trial_rows (`authoringConversation` becomes a tuple only
// with a hot source proof, else stays the saved ID with `authoringSourceLimit`).
const row = over => ({kind:'clean', content:{value:'c'}, version:'current', subAgent:null, fidelity:{state:'not checked', limits:['no fidelity reading yet']}, broughtBack:[], link:{}, standing:'s',
  authoringConversation:'thread-authoring', authoringSourceLimit:'Original authoring source is not established by this saved trial link; choose a current target', sourceLimit:null, ...over});
const producerTrials = [
  row({reference:'trial:lib-a:4', sequence:4, time:'2026-11-04 12:00', trialConversation:null}),
  row({reference:'trial:lib-a:3', sequence:3, time:'2026-11-04 11:30', trialConversation:'thread-clean-3', live:true}),
  row({reference:'trial:lib-a:2', sequence:2, time:'2026-11-04 11:00', trialConversation:'thread-clean-2', broughtBack:[{time:'2026-11-04 11:10', to:'thread-authoring'}]}),
  row({reference:'trial:lib-a:1', sequence:1, kind:'delegated', time:'2026-11-04 10:00', trialConversation:null, subAgent:{state:'sub-agent not linked'},
    authoringConversation:{generation:g, threadId:'T1'}, authoringSourceLimit:null, broughtBack:[{time:'2026-11-04 10:30', to:'thread-authoring'}, {time:'2026-11-04 10:40', to:'T1'}]}),
  {kind:'earlier attachment trial', content:{value:'abc'}, version:'earlier', conversation:'old', time:'t', link:{}},
];

test('the guide shows the draft\'s trials in host order with saved conversations as recorded, and brings one back with the draft list\'s command', async () => {
  const draft = {name:'spacing-check', state:'draft', trials:producerTrials};
  const ui = await mount({host:host(), data:data({drafts:{drafts:[draft]}})});
  await ui.name('spacing-check');
  const shown = () => region(ui.c, 'Trials of this draft').textContent;
  const order = [...shown().matchAll(/Trial (\d) ·/g)].map(m => m[1]);
  assert.deepEqual(order, ['4', '3', '2', '1'], 'the host\'s newest-first order is kept');
  assert.match(shown(), /Trial 4 · in a fresh conversation \(not started\)/, 'only an absent conversation is "not started"');
  assert.match(shown(), /Trial 2 · in a fresh conversation \(a recorded conversation \(thread-clean-2\)\) · 2026-11-04 11:00Brought back once, to a recorded conversation \(thread-authoring\)\./, 'saved bare IDs are recorded conversations, never "not started"');
  assert.match(shown(), /Trial 1 · with the agent in Conversation 1 · invented-model · 2026-11-04 10:00Brought back 2 times, to a recorded conversation \(thread-authoring\), a recorded conversation \(T1\)\./, 'a hot authoring tuple is labelled; a saved brought-back ID is not resolved against this session');
  assert.doesNotMatch(shown(), /attachment|Brought back to not started/);
  assert.equal(props(all(ui.c, 'button').find(node => node.textContent === 'Bring trial 2 back')).disabled, true, 'no conversation chosen, no bring-back');
  await ui.choose(key('T1'));
  const bring = all(ui.c, 'button').find(node => node.textContent.startsWith('Bring trial 2 back to '));
  assert.ok(bring); assert.equal(props(bring).disabled, false);
  const before = ui.calls.length;
  await React.act(async () => props(bring).onClick());
  assert.deepEqual(ui.calls.slice(before), [{command:'workflow_trial_bring_back', args:{reference:'trial:lib-a:2', generation:g, threadId:'T1', includeNative:false}}], 'exactly the draft list\'s command; nothing is sent');
  assert.equal(props(all(ui.c, 'button').find(node => node.textContent.startsWith('Bring trial 3 back'))).disabled, true); assert.match(shown(), /waits until no turn is live/);
});

test('only this draft\'s own trial results are offered; a same-name draft in another library is not', async () => {
  const draft = {name:'spacing-check', state:'draft', trials:producerTrials};
  const feedback = over => ({id:'bb-1', trial:'trial:lib-a:2', run:null, sequence:2, draftName:'spacing-check', target:{generation:g, threadId:'T1'}, source:{kind:'clean'}, prompt:'Here is how trial 2 went', transcript:'…', card:'c', textIdentity:{value:'aa'}, includeNative:false, shortenings:[], ...over});
  const pendingBringBacks = [feedback(), feedback({id:'bb-foreign', trial:'trial:lib-b:2', sequence:2}), feedback({id:'bb-other-name', trial:'trial:lib-a:9', draftName:'other-draft', sequence:9})];
  const ui = await mount({host:host({homeRouting:{activeModeHomeClass:'account'}, workflowRoot:{context:{sourceRef:'src', generation:g}, pendingBringBacks}}), data:data({drafts:{drafts:[draft]}})});
  await ui.name('spacing-check');
  await ui.choose(key('T1'));
  const shown = region(ui.c, 'Trials of this draft').textContent;
  assert.equal([...shown.matchAll(/results are ready to send/g)].length, 1, 'the same-name draft\'s results from another library are not this draft\'s');
  assert.match(shown, /Trial 2's results are ready to send in .+invented-model/);
  const calls = ui.calls.length;
  await ui.press('Read and send trial 2\'s results');
  assert.equal(ui.opened.at(-1).kind, 'bring-back'); assert.equal(ui.opened.at(-1).pending.id, 'bb-1');
  assert.equal(ui.calls.length, calls, 'opening issues no command and sends nothing');
});

const doubtsModule = loadSrc('bringBackDoubts');
const results = over => ({id:'bb-1', trial:'trial:lib-a:2', run:null, sequence:2, draftName:'spacing-check', target:{generation:g, threadId:'T1'}, source:{kind:'clean'}, prompt:'p', transcript:'…', card:'c', textIdentity:{value:'aa'}, includeNative:false, shortenings:[], ...over});
const doubt = over => ({kind:'trial', ref:'trial:lib-a:2', sequence:2, draftName:'spacing-check', preparedId:'bb-1', source:{sourceRef:'src', modeHomeClass:'account', generation:g},
  target:{generation:g, threadId:'T1'}, personText:'My edited prompt for trial 2', message:'invented: The transcript was sent (turn t) but its brought-back observation could not be written. Nothing is resent', brought:1, acknowledged:false, ...over});

test('an identical prepared bring-back is opened instead of made again, a double press makes one, and the new results take focus', async () => {
  doubtsModule.resetBringBackDoubts();
  const proto = Object.getPrototypeOf(document.createElement('button')); const focused = []; const previousFocus = proto.focus;
  proto.focus = function () { focused.push(this); };
  try {
    const draft = {name:'spacing-check', state:'draft', trials:producerTrials};
    const ui = await mount({host:host({homeRouting:{activeModeHomeClass:'account'}}), data:data({drafts:{drafts:[draft]}})});
    await ui.name('spacing-check'); await ui.choose(key('T1'));
    const bring = n => all(ui.c, 'button').find(node => node.textContent.startsWith(`Bring trial ${n} back`));
    const onClick = props(bring(2)).onClick;
    const before = ui.calls.length;
    await React.act(async () => { onClick(); onClick(); });
    assert.equal(ui.calls.slice(before).filter(call => call.command === 'workflow_trial_bring_back').length, 1, 'a double press makes one bring-back');
    await ui.rerender({host:host({homeRouting:{activeModeHomeClass:'account'}, workflowRoot:{context:{sourceRef:'src', generation:g}, pendingBringBacks:[results()]}})});
    assert.equal(focused.at(-1)?.textContent, 'Read and send trial 2\'s results', 'the new results message takes the focus');
    assert.equal(bring(2), undefined, 'no second pre-fill for the same conversation');
    assert.match(region(ui.c, 'Trial 2 of spacing-check').textContent, /Its results are already prepared for this conversation/);
    const calls = ui.calls.length;
    await ui.press('Read and send trial 2\'s prepared results');
    assert.equal(ui.opened.at(-1).pending.id, 'bb-1', 'the existing prepared message is opened'); assert.equal(ui.calls.length, calls, 'nothing new is made or sent');
    await ui.rerender({host:host({homeRouting:{activeModeHomeClass:'account'}, workflowRoot:{context:{sourceRef:'src', generation:g}, pendingBringBacks:[results({target:{generation:g, threadId:'T2'}})]}})});
    assert.ok(bring(2), 'results prepared for another conversation do not forbid a distinct bring-back here');
  } finally { proto.focus = previousFocus; doubtsModule.resetBringBackDoubts(); }
});

test('an unconfirmed bring-back send holds that trial and conversation ID in the guide and the studio until checked, across a restart or home change, and keeps the original outcome', async () => {
  doubtsModule.resetBringBackDoubts();
  const draft = {name:'spacing-check', state:'draft', trials:producerTrials};
  const view = {host:host({homeRouting:{activeModeHomeClass:'account'}}), data:data({drafts:{drafts:[draft]}})};
  const ui = await mount(view);
  await ui.name('spacing-check'); await ui.choose(key('T1'));
  const bring = n => all(ui.c, 'button').find(node => node.textContent.startsWith(`Bring trial ${n} back`));
  const earlierBring = props(bring(2)).onClick;
  await React.act(async () => doubtsModule.noteBringBackDoubt(doubt()));
  const alert = () => region(ui.c, 'Trial 2 results may have been sent');
  assert.ok(alert()); assert.equal(alert().getAttribute('role'), 'alert');
  assert.match(alert().textContent, /Trial 2's results may already have been sent to .+invented-model.+could send the transcript twice\..*Your message: My edited prompt for trial 2.*Reported: .*observation could not be written.*Original destination: conversation T1/);
  assert.equal(props(bring(2)).disabled, true, 'held: no blind second bring-back');
  assert.match(next(ui.c), /spacing-check: Check whether trial 2's results arrived in the conversation before bringing it back again/, 'the top Next is the actual step');
  const before = ui.calls.length;
  await React.act(async () => { earlierBring(); });
  assert.equal(ui.calls.length, before, 'a control from before the doubt cannot bring it back');
  // A later bring-back recorded to ANOTHER conversation is no evidence for this one.
  const toB = producerTrials.map(row => row.reference === 'trial:lib-a:2' ? {...row, broughtBack:[...row.broughtBack, {time:'later', to:'T2'}]} : row);
  await ui.rerender({data:data({drafts:{drafts:[{...draft, trials:toB}]}})});
  assert.equal(props(bring(2)).disabled, true, 'A stays held after a record for B');
  // Even a record naming the same bare ID is not this send's receipt.
  const toA = producerTrials.map(row => row.reference === 'trial:lib-a:2' ? {...row, broughtBack:[...row.broughtBack, {time:'later', to:'T1'}]} : row);
  await ui.rerender({data:data({drafts:{drafts:[{...draft, trials:toA}]}})});
  assert.equal(props(bring(2)).disabled, true, 'no count or bare-ID record releases the hold');
  // A Codex restart (same home) and a home change keep the hold for the same conversation ID.
  for (const generation of [{...g, spawnCounter:2}, {...g, home:'api-key', spawnCounter:5}]) {
    await ui.rerender({host:host({generation, homeRouting:{activeModeHomeClass:generation.home === 'api-key' ? 'api-key' : 'account'}, workflowRoot:{context:{sourceRef:'src', generation}},
      threads:[{threadId:'T1', generation, model:'invented-model'}, {threadId:'T2', generation, model:'invented-model'}]}), data:data({context:{sourceRef:'src', generation}, drafts:{drafts:[draft]}})});
    await ui.choose(JSON.stringify([generation, 'T1']));
    assert.ok(alert(), 'a source change does not erase the record');
    assert.match(alert().textContent, /sent to a conversation that isn't loaded now.*Codex or the home has changed since that send\. The conversation chosen now has the same ID \(T1\), so bringing trial 2 back to it is held until you've checked\. That doesn't make the earlier destination this one\./);
    assert.equal(props(bring(2)).disabled, true, `held for the same conversation ID after ${generation.home === 'api-key' ? 'a home change' : 'a restart'}`);
    await ui.choose(JSON.stringify([generation, 'T2']));
    assert.equal(props(bring(2)).disabled, false, 'a different, explicitly chosen conversation is not held');
    await ui.choose(JSON.stringify([generation, 'T1']));
  }
  // The studio's draft list shares the hold, and reads the host's pending rows by their `target`.
  const {TrialRow} = loadSrc('WorkflowDrafts');
  const studioCalls = [];
  const studioRow = (over = {}) => TrialRow({trial:producerTrials[2], conversations:[{threadId:'T1', generation:g, model:'m'}, {threadId:'T2', generation:g, model:'m'}], busy:false, act:(command, args) => { studioCalls.push({command, args}); },
    state:{chosen:[], bbTarget:{'trial:lib-a:2':key('T1')}, bbNative:{}}, update:() => {}, ...over});
  const find = (node, out = []) => { if (Array.isArray(node)) { node.forEach(n => find(n, out)); return out; } if (!node || typeof node !== 'object') return out; if (node.type === 'button') out.push(node); find(node.props?.children, out); return out; };
  const studioBring = tree => find(tree).find(node => [].concat(node.props.children).join('') === 'Bring trial back');
  assert.equal(studioBring(studioRow()).props.disabled, true); studioBring(studioRow()).props.onClick();
  assert.deepEqual(studioCalls, [], 'the studio refuses at the press too');
  await ui.press('I\'ve checked — let me bring it back again');
  assert.equal(ui.calls.length, before, 'acknowledging starts nothing');
  assert.equal(props(bring(2)).disabled, false, 'only the explicit acknowledgement lifts the hold');
  assert.match(alert().textContent, /You said you checked that conversation\..*Your message: My edited prompt/, 'the original outcome stays shown');
  const pendingHere = {id:'bb-guide', trial:'trial:lib-a:2', run:null, sequence:2, draftName:'spacing-check', target:{generation:g, threadId:'T1'}, includeNative:false};
  assert.equal(studioBring(studioRow({bringBacks:[pendingHere]})).props.disabled, true, 'a result the guide prepared for T1 disables the studio\'s identical bring-back');
  assert.equal(studioBring(studioRow({bringBacks:[{...pendingHere, target:{generation:g, threadId:'T2'}}]})).props.disabled, false, 'a result for another conversation does not');
  doubtsModule.resetBringBackDoubts();
});

test('the dispatch guard reads the host\'s current view: a published identical preparation, a held doubt or a send in flight issues nothing', () => {
  doubtsModule.resetBringBackDoubts();
  const {bringBackRefusal, beginBringBack, endBringBack, sendKey} = doubtsModule;
  const current = pending => ({workflowRoot:{pendingBringBacks:pending}});
  const prepare = {reference:'trial:lib-a:2', generation:g, threadId:'T1', includeNative:false};
  assert.equal(bringBackRefusal('workflow_trial_bring_back', prepare, current([])), null);
  assert.match(bringBackRefusal('workflow_trial_bring_back', prepare, current([results({id:'bb-1'})])), /already prepared for that conversation/, 'a retained Bring after the preparation was published');
  assert.equal(bringBackRefusal('workflow_trial_bring_back', {...prepare, includeNative:true}, current([results({id:'bb-1'})])), null, 'different options are a distinct intent');
  assert.equal(bringBackRefusal('workflow_run_bring_back', {runRef:'run-1', generation:g, threadId:'T1', includeNative:false}, current([results({id:'bb-r', trial:null, run:'run-1'})])) !== null, true);
  const two = current([results({id:'bb-1'}), results({id:'bb-2'})]);
  assert.equal(beginBringBack(sendKey('trial', 'trial:lib-a:2', {generation:g, threadId:'T1'})), true);
  assert.match(bringBackRefusal('workflow_bring_back_send', {id:'bb-2', generation:g, threadId:'T1'}, two), /being sent to this conversation now/, 'a second composer while the first is in flight');
  endBringBack(sendKey('trial', 'trial:lib-a:2', {generation:g, threadId:'T1'}));
  doubtsModule.noteBringBackDoubt(doubt({preparedId:'bb-1', target:{generation:g, threadId:'T1'}}));
  assert.match(bringBackRefusal('workflow_bring_back_send', {id:'bb-2', generation:g, threadId:'T1'}, two), /wasn't confirmed and may have arrived/, 'the second composer after the first one\'s unknown outcome');
  assert.match(bringBackRefusal('workflow_bring_back_send', {id:'bb-2', generation:{...g, spawnCounter:2}, threadId:'T1'}, two), /wasn't confirmed/, 'the same conversation ID after a restart');
  assert.equal(bringBackRefusal('workflow_bring_back_send', {id:'bb-2', generation:g, threadId:'T2'}, two), null, 'another conversation');
  doubtsModule.resetBringBackDoubts();
});

test('registration guidance follows the review\'s own identity and status, never the draft state alone', async () => {
  doubtsModule.resetBringBackDoubts();
  const presentation = {library:'/invented/project', origin:'project', entries:[{identity:{name:'spacing-check'}, disposition:'new'}]};
  const ui = await mount({host:host(), data:data({activeReview:'review:1', reviews:[{reference:'review:1', status:{state:'reviewed', presentation}}], drafts:{drafts:[{name:'spacing-check', state:'under review'}]}})});
  await ui.name('spacing-check'); await ui.choose(key('T1'));
  assert.match(next(ui.c), /A review is open\. Read it and confirm registration in the App's dialog/, 'the review is current and shown');
  await ui.rerender({data:data({activeReview:'review:1', reviews:[{reference:'review:1', status:{state:'native confirmation dismissed; no capture/registration'}}], drafts:{drafts:[{name:'spacing-check', state:'under review'}]}})});
  assert.match(next(ui.c), /You cancelled the App's confirmation, so nothing was registered/, 'a dismissed confirmation is said so even while the draft observation is cached');
  assert.doesNotMatch(region(ui.c, 'Draft status').textContent, /confirm registration in the App's dialog/);
  await ui.rerender({data:data({activeReview:'review:1', reviews:[{reference:'review:1', status:{state:'native review/capture unavailable; original owner state retained', limit:'invented capture limit', registration:'not completed; no fabricated receipt or retry'}}], drafts:{drafts:[{name:'spacing-check', state:'under review'}]}})});
  assert.match(next(ui.c), /registration did not complete \(invented capture limit\)\. The original attempt is kept: continue it from the review, or review the draft again/);
  assert.doesNotMatch(region(ui.c, 'Draft status').textContent, /confirm registration in the App's dialog|Registered/);
  await ui.rerender({data:data({activeReview:'review:2', reviews:[{reference:'review:1', status:{state:'reviewed', presentation}}, {reference:'review:2', status:{state:'reviewed', presentation:{library:'/invented/project', origin:'project', entries:[{identity:{name:'other-draft'}}]}}}], drafts:{drafts:[{name:'spacing-check', state:'under review'}]}})});
  assert.match(next(ui.c), /That review is no longer the current one, so it can't be confirmed from here/, 'another draft\'s current review does not stand for this one');
});

test('a review from another library never guides a same-name draft after switching libraries', async () => {
  const presentation = (library, origin = 'project') => ({review_ref:'r', library, origin, source_root:'src-root', entries:[{identity:{name:'spacing-check', origin, source_root:'src-root'}, disposition:'new'}]});
  const libA = {reference:'lib:project', origin:'project', root:path('/invented/project'), sourceRoot:'src-root', registered:[]};
  const libB = {reference:'lib:other', origin:'project', root:path('/invented/other'), sourceRoot:'src-root', registered:[]};
  const draft = {name:'spacing-check', state:'draft'};
  const ui = await mount({host:host(), data:data({libraries:[libA, libB], activeLibrary:'lib:project', activeReview:'review:a', reviews:[{reference:'review:a', status:{state:'reviewed', presentation:presentation('/invented/project')}}], drafts:{drafts:[{...draft, state:'under review'}]}})});
  await ui.name('spacing-check'); await ui.choose(key('T1'));
  assert.match(next(ui.c), /A review is open\. Read it and confirm registration/, 'library A\'s review guides library A\'s draft');
  for (const status of [{state:'reviewed', presentation:presentation('/invented/project')}, {state:'native confirmation dismissed; no capture/registration'}, {state:'native review/capture unavailable; original owner state retained', limit:'x'}]) {
    await ui.rerender({data:data({libraries:[libA, libB], activeLibrary:'lib:other', activeReview:'review:a', reviews:[{reference:'review:a', status}], drafts:{drafts:[draft]}})});
    const shown = region(ui.c, 'Draft status').textContent;
    assert.doesNotMatch(shown, /A review is open|You cancelled|became unavailable|See the review|Open the review/, `library B's same-name draft is not guided by A's review (${status.state})`);
    assert.match(next(ui.c), /spacing-check: Optionally try it/);
  }
});

test('a prepared copy whose send is held is offered for reading or removing, never as ready to send', async () => {
  doubtsModule.resetBringBackDoubts();
  const draft = {name:'spacing-check', state:'draft', trials:producerTrials};
  const ui = await mount({host:host({homeRouting:{activeModeHomeClass:'account'}, workflowRoot:{context:{sourceRef:'src', generation:g}, pendingBringBacks:[results()]}}), data:data({drafts:{drafts:[draft]}})});
  await ui.name('spacing-check'); await ui.choose(key('T1'));
  const shown = () => region(ui.c, 'Trials of this draft').textContent;
  assert.match(shown(), /Trial 2's results are ready to send in/);
  await React.act(async () => doubtsModule.noteBringBackDoubt(doubt({preparedId:'bb-1'})));
  assert.doesNotMatch(shown(), /ready to send/, 'a held copy is not "ready to send"');
  assert.match(shown(), /Trial 2's results are prepared in .+, but sending them is held: this copy's earlier send wasn't confirmed and may have arrived, so it is not sent again\./);
  assert.ok(button(ui.c, 'Open trial 2\'s prepared results to read or remove'));
  await React.act(async () => { doubtsModule.acknowledgeBringBackDoubt(doubtsModule.bringBackDoubtsFor('trial', 'trial:lib-a:2')[0]); });
  assert.match(shown(), /prepared in .+, but sending them is held/, 'that attempted copy stays held after the acknowledgement');
  assert.match(next(ui.c), /Trial 2's prepared results are held and not sent again; after reading the conversation, remove that copy/);
  const calls = ui.calls.length;
  await ui.press('Open trial 2\'s prepared results to read or remove');
  assert.equal(ui.opened.at(-1).pending.id, 'bb-1'); assert.equal(ui.calls.length, calls, 'opening issues nothing');
  doubtsModule.resetBringBackDoubts();
});
